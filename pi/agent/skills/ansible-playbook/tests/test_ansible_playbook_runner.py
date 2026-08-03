"""
Unit tests for Ansible Playbook Runner

Run with: pytest tests/test_ansible_playbook_runner.py -v
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest
import yaml

from ansible_playbook_runner import PlaybookRunner


@pytest.fixture
def temp_cassandra_root(tmp_path):
    """Create temporary cassandra-ansible directory structure."""
    playbooks_dir = tmp_path / "playbooks"
    inventories_dir = tmp_path / "inventories"
    
    playbooks_dir.mkdir()
    inventories_dir.mkdir()
    
    # Create sample playbooks
    playbook1 = playbooks_dir / "test_playbook.yml"
    playbook1.write_text(yaml.dump([
        {
            "name": "Test Play",
            "hosts": "{{ datacenter_name }}",
            "vars": {
                "datacenter_name": None,  # Required
                "optional_var": "default"
            },
            "tasks": [
                {"name": "Test task", "debug": {"msg": "Hello"}}
            ]
        }
    ]))
    
    playbook2 = playbooks_dir / "simple_playbook.yml"
    playbook2.write_text(yaml.dump([
        {
            "name": "Simple Play",
            "hosts": "all",
            "tasks": [
                {"name": "Simple task", "debug": {"msg": "Hi"}}
            ]
        }
    ]))
    
    # Create inventory structure
    qa_dir = inventories_dir / "qa" / "group_vars"
    qa_dir.mkdir(parents=True)
    (inventories_dir / "qa" / "all.yml").write_text("---\ncluster: test-cluster\n")
    
    return tmp_path


@pytest.fixture
def runner(temp_cassandra_root):
    """Create PlaybookRunner with temp directory."""
    return PlaybookRunner(
        cassandra_root=str(temp_cassandra_root),
        disable_opensearch=True
    )


class TestPlaybookDiscovery:
    """Test playbook discovery functionality."""

    def test_discover_playbooks(self, runner):
        """Test discovering all playbooks."""
        playbooks = runner.discover_playbooks()
        
        assert len(playbooks) == 2
        assert "test_playbook" in playbooks
        assert "simple_playbook" in playbooks

    def test_discover_playbooks_empty_dir(self, tmp_path):
        """Test discovery with no playbooks."""
        runner = PlaybookRunner(cassandra_root=str(tmp_path), disable_opensearch=True)
        (tmp_path / "playbooks").mkdir()
        
        playbooks = runner.discover_playbooks()
        assert len(playbooks) == 0

    def test_discover_playbooks_missing_dir(self):
        """Test discovery with missing directory."""
        runner = PlaybookRunner(cassandra_root="/nonexistent", disable_opensearch=True)
        
        with pytest.raises(FileNotFoundError):
            runner.discover_playbooks()


class TestClusterDiscovery:
    """Test cluster discovery functionality."""

    def test_discover_clusters_from_file(self, temp_cassandra_root):
        """Test discovering clusters from files."""
        # Create clusters directory with test files
        clusters_dir = temp_cassandra_root / "clusters"
        clusters_dir.mkdir()
        (clusters_dir / "test-cluster-1").touch()
        (clusters_dir / "test-cluster-2").touch()
        (clusters_dir / ".gitignore").touch()  # Should be ignored
        
        runner = PlaybookRunner(cassandra_root=str(temp_cassandra_root), disable_opensearch=True)
        clusters = runner.discover_clusters()
        
        assert len(clusters) == 2
        assert "test-cluster-1" in clusters
        assert "test-cluster-2" in clusters
        assert ".gitignore" not in clusters

    def test_discover_clusters_fallback(self, temp_cassandra_root):
        """Test cluster discovery fallback to defaults."""
        runner = PlaybookRunner(cassandra_root=str(temp_cassandra_root), disable_opensearch=True)
        clusters = runner.discover_clusters()
        
        # Should return default when no clusters directory
        assert len(clusters) >= 1
        assert "piotr-test-cluster" in clusters


class TestVariableParsing:
    """Test playbook variable parsing."""

    def test_parse_required_variables(self, runner):
        """Test extracting required variables."""
        vars_list = runner.parse_required_variables("test_playbook")
        
        assert "datacenter_name" in vars_list

    def test_parse_simple_playbook(self, runner):
        """Test parsing playbook with no special variables."""
        vars_list = runner.parse_required_variables("simple_playbook")
        
        assert len(vars_list) == 0

    def test_parse_nonexistent_playbook(self, runner):
        """Test parsing non-existent playbook."""
        vars_list = runner.parse_required_variables("nonexistent")
        
        assert len(vars_list) == 0

    def test_parse_invalid_yaml(self, runner):
        """Test parsing invalid YAML."""
        playbook_path = runner.playbooks_dir / "invalid.yml"
        playbook_path.write_text("{ invalid yaml ][")
        
        vars_list = runner.parse_required_variables("invalid")
        
        assert len(vars_list) == 0


class TestLiveConfirmation:
    """Test live environment confirmation."""

    def test_confirm_live_execution_success(self, runner, monkeypatch):
        """Test successful live confirmation."""
        monkeypatch.setattr("builtins.input", 
                           lambda _: runner.CONFIRMATION_STRING)
        
        result = runner.confirm_live_execution()
        assert result is True

    def test_confirm_live_execution_failure(self, runner, monkeypatch):
        """Test failed live confirmation."""
        monkeypatch.setattr("builtins.input", 
                           lambda _: "wrong confirmation")
        
        result = runner.confirm_live_execution()
        assert result is False


class TestLogFormatting:
    """Test log formatting per logback pattern."""

    def test_format_logback_message(self, runner):
        """Test logback format string generation."""
        message = runner.format_logback_message("INFO", "Test message")
        
        # Check format: ISO8601 LEVEL [thread] message
        assert "T" in message  # ISO8601 has T
        assert "Z" in message  # ISO8601 ends with Z
        assert "INFO " in message
        assert "[main]" in message
        assert "Test message" in message

    def test_format_logback_error_level(self, runner):
        """Test error level formatting."""
        message = runner.format_logback_message("ERROR", "Something failed")
        
        assert "ERROR" in message
        assert "Something failed" in message


class TestOpenSearchExport:
    """Test OpenSearch export functionality."""

    def test_export_disabled(self, runner):
        """Test export when disabled."""
        runner.disable_opensearch = True
        
        result = runner.export_to_opensearch(
            "test_playbook",
            "qa",
            {},
            0,
            "stdout",
            "stderr",
            1.0
        )
        
        assert result is True

    def test_export_creates_log_file(self, runner):
        """Test that export creates local log file."""
        result = runner.export_to_opensearch(
            "test_playbook",
            "qa",
            {"datacenter": "test"},
            0,
            "test stdout",
            "test stderr",
            2.5
        )
        
        # Should at least save locally
        log_files = list(runner.LOG_DIR.glob("*.jsonl"))
        assert len(log_files) > 0

    def test_export_log_entry_format(self, runner):
        """Test exported log entry format."""
        runner.export_to_opensearch(
            "test_playbook",
            "qa",
            {"datacenter": "test"},
            0,
            "test output",
            "",
            1.5
        )
        
        # Read exported log
        log_files = list(runner.LOG_DIR.glob("*.jsonl"))
        assert len(log_files) > 0
        
        with open(log_files[0]) as f:
            entry = json.loads(f.read().strip())
        
        assert entry["playbook"] == "test_playbook"
        assert entry["stage"] == "qa"
        assert entry["status"] == "success"
        assert entry["returncode"] == 0
        assert entry["duration_seconds"] == 1.5
        assert "timestamp" in entry
        assert "level" in entry


class TestPlaybookExecution:
    """Test playbook execution."""

    @patch("subprocess.run")
    def test_run_playbook_success(self, mock_run, runner):
        """Test successful playbook execution."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Playbook ran successfully"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        code, stdout, stderr = runner.run_playbook("test_playbook", "qa", {})
        
        assert code == 0
        assert stdout == "Playbook ran successfully"
        assert stderr == ""
        mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_run_playbook_failure(self, mock_run, runner):
        """Test failed playbook execution."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = "Some output"
        mock_result.stderr = "Connection error"
        mock_run.return_value = mock_result
        
        code, stdout, stderr = runner.run_playbook("test_playbook", "qa", {})
        
        assert code == 1
        assert stderr == "Connection error"

    @patch("subprocess.run", side_effect=subprocess.TimeoutExpired("cmd", 3600))
    def test_run_playbook_timeout(self, mock_run, runner):
        """Test playbook execution timeout."""
        code, stdout, stderr = runner.run_playbook("test_playbook", "qa", {})
        
        assert code == 124  # Timeout exit code
        assert "timed out" in stderr

    @patch("subprocess.run", side_effect=Exception("System error"))
    def test_run_playbook_system_error(self, mock_run, runner):
        """Test playbook execution with system error."""
        code, stdout, stderr = runner.run_playbook("test_playbook", "qa", {})
        
        assert code == 1
        assert "System error" in stderr


class TestDirectMode:
    """Test direct CLI mode."""

    @patch.object(PlaybookRunner, "run_playbook")
    def test_direct_mode_qa(self, mock_run, runner):
        """Test direct mode with QA stage."""
        mock_run.return_value = (0, "success", "")
        
        code = runner.direct_mode("test_playbook", {"stage": "qa"})
        
        assert code == 0
        mock_run.assert_called_once()

    @patch.object(PlaybookRunner, "confirm_live_execution", return_value=False)
    def test_direct_mode_live_cancelled(self, mock_confirm, runner):
        """Test direct mode with cancelled live confirmation."""
        code = runner.direct_mode("test_playbook", {"stage": "live"})
        
        assert code == 1

    @patch.object(PlaybookRunner, "confirm_live_execution", return_value=True)
    @patch.object(PlaybookRunner, "run_playbook")
    def test_direct_mode_live_confirmed(self, mock_run, mock_confirm, runner):
        """Test direct mode with confirmed live execution."""
        mock_run.return_value = (0, "success", "")
        
        code = runner.direct_mode("test_playbook", {"stage": "live"})
        
        assert code == 0
        mock_confirm.assert_called_once()
        mock_run.assert_called_once()


class TestInteractiveMode:
    """Test interactive mode."""

    def test_interactive_mode_no_playbooks(self, tmp_path):
        """Test interactive mode with no playbooks."""
        runner = PlaybookRunner(cassandra_root=str(tmp_path), disable_opensearch=True)
        (tmp_path / "playbooks").mkdir()
        (tmp_path / "inventories").mkdir()
        
        code = runner.interactive_mode()
        
        assert code == 1

    @patch.object(PlaybookRunner, "run_playbook")
    @patch("builtins.input")
    def test_interactive_mode_qa_flow(self, mock_input, mock_run, runner):
        """Test interactive mode QA flow."""
        # Mock user input: select first playbook, QA stage, no additional vars needed
        mock_input.side_effect = ["1", "1", ""]
        mock_run.return_value = (0, "success", "")
        
        code = runner.interactive_mode()
        
        # Should succeed
        assert code == 0


# Import for TestPlaybookExecution
import subprocess


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

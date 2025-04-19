import yaml

def test_config_parsing():
    with open("config/config.yaml") as f:
        config = yaml.safe_load(f)
    
    assert config["app_name"] == "LogNotifier"
    assert "logging" in config
    print("✅ Config parsed successfully.")

if __name__ == "__main__":
    test_config_parsing()

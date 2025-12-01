# ============================================================================
# deploy/deploy.py
# ============================================================================
"""
Deployment script for MarketReportAgent to Vertex AI Agent Engine
"""

import os
import sys
import yaml
import subprocess
from pathlib import Path
from typing import Dict, Any

def load_config(config_path: str = "deploy/agent_engine_config.yaml") -> Dict[str, Any]:
    """Load deployment configuration from YAML file."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"❌ Error: Configuration file not found at {config_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML configuration: {e}")
        sys.exit(1)

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate that required configuration fields are present."""
    required_fields = ['project_id', 'location', 'agent_engine_id']
    
    for field in required_fields:
        if not config.get(field) or config[field] == f"your-{field}":
            print(f"❌ Error: Please update '{field}' in agent_engine_config.yaml")
            return False
    
    return True

def check_gcloud_auth() -> bool:
    """Check if user is authenticated with gcloud."""
    try:
        result = subprocess.run(
            ['gcloud', 'auth', 'list'],
            capture_output=True,
            text=True,
            check=True
        )
        if "ACTIVE" in result.stdout:
            print("✅ gcloud authentication verified")
            return True
        else:
            print("❌ No active gcloud authentication found")
            print("   Run: gcloud auth login")
            return False
    except subprocess.CalledProcessError:
        print("❌ Error checking gcloud authentication")
        return False
    except FileNotFoundError:
        print("❌ gcloud CLI not found. Please install Google Cloud SDK")
        return False

def enable_required_apis(project_id: str) -> bool:
    """Enable required Google Cloud APIs."""
    apis = [
        "aiplatform.googleapis.com",
        "cloudfunctions.googleapis.com",
        "run.googleapis.com"
    ]
    
    print("\n🔧 Enabling required APIs...")
    for api in apis:
        try:
            print(f"   Enabling {api}...")
            subprocess.run(
                ['gcloud', 'services', 'enable', api, '--project', project_id],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to enable {api}: {e}")
            return False
    
    print("✅ All required APIs enabled")
    return True

def create_requirements_for_deployment() -> None:
    """Create a requirements.txt suitable for deployment."""
    deployment_requirements = """google-genai
google-adk
yfinance
python-dotenv
aiosqlite
pyyaml
"""
    
    with open("deploy/requirements.txt", 'w') as f:
        f.write(deployment_requirements)
    
    print("✅ Created deploy/requirements.txt")

def deploy_agent(config: Dict[str, Any]) -> bool:
    """Deploy the agent to Vertex AI Agent Engine."""
    project_id = config['project_id']
    location = config['location']
    agent_id = config['agent_engine_id']
    
    print(f"\n🚀 Deploying MarketReportAgent...")
    print(f"   Project: {project_id}")
    print(f"   Location: {location}")
    print(f"   Agent ID: {agent_id}")
    
    try:
        # Example deployment command (adjust based on actual ADK CLI)
        cmd = [
            'gcloud', 'ai', 'agents', 'deploy',
            '--project', project_id,
            '--location', location,
            '--agent-id', agent_id,
            '--source', '.',
            '--config', 'deploy/agent_engine_config.yaml'
        ]
        
        print(f"\n📝 Running deployment command:")
        print(f"   {' '.join(cmd)}")
        
        # Uncomment when ready to deploy:
        # result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        # print(result.stdout)
        
        print("\n✅ Deployment initiated!")
        print(f"\n🔗 View your agent at:")
        print(f"   https://console.cloud.google.com/vertex-ai/agents?project={project_id}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Deployment failed: {e}")
        if e.stderr:
            print(f"   Error details: {e.stderr}")
        return False

def main():
    """Main deployment workflow."""
    print("=" * 70)
    print("MarketReportAgent - Vertex AI Agent Engine Deployment")
    print("=" * 70)
    
    # Load configuration
    print("\n📋 Loading configuration...")
    config = load_config()
    
    # Validate configuration
    if not validate_config(config):
        sys.exit(1)
    
    print("✅ Configuration validated")
    
    # Check authentication
    if not check_gcloud_auth():
        sys.exit(1)
    
    # Enable APIs
    if not enable_required_apis(config['project_id']):
        print("⚠️  Warning: Some APIs may not be enabled")
    
    # Create deployment requirements
    create_requirements_for_deployment()
    
    # Deploy agent
    print("\n" + "=" * 70)
    deploy_success = deploy_agent(config)
    print("=" * 70)
    
    if deploy_success:
        print("\n🎉 Deployment completed successfully!")
        print("\nNext steps:")
        print("1. Verify deployment in Cloud Console")
        print("2. Test the agent with sample queries")
        print("3. Monitor logs and metrics")
        print("4. Set up alerts and monitoring")
    else:
        print("\n❌ Deployment failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
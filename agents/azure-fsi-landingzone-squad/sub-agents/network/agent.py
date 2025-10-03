"""Network Specialist Sub-Agent for Azure FSI Landing Zone."""
import asyncio, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))
from shared.agents import BaseClaudeAgent
from shared.utils import setup_logging
from claude_agent_sdk import tool

class NetworkSpecialistAgent(BaseClaudeAgent):
    """Network specialist for FSI Landing Zone architecture."""
    
    def get_system_prompt(self):
        return """You are a Network Architecture expert for Azure FSI Landing Zones.
        
Expertise: Hub-spoke topology, Azure Firewall, VPN Gateway, Private Endpoints, VNet peering, routing, DNS.
Focus on: Network segmentation, zero-trust architecture, private connectivity, traffic inspection."""

    def get_custom_tools(self):
        return [self.analyze_network_topology, self.review_firewall_rules]
    
    @tool("analyze_network_topology", "Analyze hub-spoke network topology", {})
    async def analyze_network_topology(self, args):
        return {"content": [{"type": "text", "text": "🌐 Network Topology Analysis\n\nHub-Spoke architecture review for FSI compliance..."}]}
    
    @tool("review_firewall_rules", "Review Azure Firewall rules", {})
    async def review_firewall_rules(self, args):
        return {"content": [{"type": "text", "text": "🔥 Azure Firewall Rules Review\n\nAnalyzing firewall policies..."}]}

async def main():
    print("\n🌐 NETWORK SPECIALIST AGENT\nSpecialization: Network Architecture, Hub-Spoke, Firewall")
    print("⚠️  Sub-agent - invoke via orchestrator\n")

if __name__ == "__main__":
    asyncio.run(main())

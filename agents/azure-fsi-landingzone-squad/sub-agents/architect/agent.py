"""Architect Specialist Sub-Agent for Azure FSI Landing Zone."""
import asyncio, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))
from shared.agents import BaseClaudeAgent
from shared.utils import setup_logging
from claude_agent_sdk import tool

class ArchitectSpecialistAgent(BaseClaudeAgent):
    """Solution Architect specialist - synthesizes multi-domain insights."""
    
    def get_system_prompt(self):
        return """You are a Solution Architect expert for Azure FSI Landing Zones.
        
Expertise: Overall architecture design, cross-domain synthesis, best practices, cost optimization, trade-off analysis.
Role: Synthesize insights from DevOps, Security, and Network specialists into actionable recommendations."""

    def get_custom_tools(self):
        return [self.synthesize_analysis, self.recommend_improvements]
    
    @tool("synthesize_analysis", "Synthesize multi-agent analysis into overall assessment", {"analyses": str})
    async def synthesize_analysis(self, args):
        return {"content": [{"type": "text", "text": "🏗️  Architecture Synthesis\n\nOverall assessment and recommendations..."}]}
    
    @tool("recommend_improvements", "Recommend architecture improvements", {})
    async def recommend_improvements(self, args):
        return {"content": [{"type": "text", "text": "💡 Architecture Improvement Recommendations\n\nPrioritized action items..."}]}

async def main():
    print("\n🏗️  ARCHITECT SPECIALIST AGENT\nSpecialization: Solution Architecture, Synthesis, Best Practices")
    print("⚠️  Sub-agent - invoke via orchestrator\n")

if __name__ == "__main__":
    asyncio.run(main())

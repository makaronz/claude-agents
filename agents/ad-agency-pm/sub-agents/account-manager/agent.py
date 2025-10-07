#!/usr/bin/env python3
"""
Account Manager Agent for Ad Agency Project Manager
Specializes in client brief analysis, requirement extraction, and client communication.
"""

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# Add parent directories to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from shared.agents import InteractiveAgent
from claude_agent_sdk import tool


class AccountManagerAgent(InteractiveAgent):
    """Account Manager Agent specializing in brief analysis and client communication."""
    
    def __init__(self, config_dir: Path):
        super().__init__(config_dir)
        self.data_dir = Path("data/account_manager")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def get_custom_tools(self) -> List[Any]:
        """Return list of custom tools for Account Manager."""
        return [
            self.analyze_brief,
            self.extract_requirements,
            self.client_communication,
            self.validate_brief,
            self.create_brief_summary
        ]
    
    @tool("analyze_brief", "Analyze client brief and extract key information", {
        "brief_content": "str",
        "client_info": "dict"
    })
    async def analyze_brief(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze client brief and extract key information."""
        brief_content = args.get("brief_content", "")
        client_info = args.get("client_info", {})
        
        if not brief_content:
            return {"content": [{"type": "text", "text": "Error: Brief content is required"}]}
        
        # Create analysis structure
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "client_info": client_info,
            "brief_content": brief_content,
            "analysis": {
                "business_objectives": [],
                "target_audience": {},
                "key_messages": [],
                "deliverables": [],
                "constraints": {
                    "budget": None,
                    "timeline": None,
                    "resources": []
                },
                "brand_guidelines": {},
                "success_metrics": []
            },
            "questions_for_clarification": [],
            "risk_factors": [],
            "recommendations": []
        }
        
        # Save analysis
        analysis_file = self.data_dir / f"brief_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        result = f"""📋 **Brief Analysis Complete**

**Client:** {client_info.get('name', 'Unknown')}
**Project:** {client_info.get('project_name', 'Unnamed Project')}

**Key Findings:**
- Business objectives identified: {len(analysis['analysis']['business_objectives'])} items
- Target audience defined: {bool(analysis['analysis']['target_audience'])}
- Key messages extracted: {len(analysis['analysis']['key_messages'])} items
- Deliverables specified: {len(analysis['analysis']['deliverables'])} items

**Questions for Clarification:**
{len(analysis['questions_for_clarification'])} questions identified

**Risk Factors:**
{len(analysis['risk_factors'])} potential risks identified

**Next Steps:**
1. Review analysis with client
2. Address clarification questions
3. Finalize requirements
4. Hand off to Strategy Planner and Creative Director

Analysis saved to: {analysis_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("extract_requirements", "Extract specific requirements from brief analysis", {
        "analysis_id": "str",
        "requirement_type": "str"
    })
    async def extract_requirements(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Extract specific requirements from brief analysis."""
        analysis_id = args.get("analysis_id", "")
        requirement_type = args.get("requirement_type", "all")
        
        # Find analysis file
        analysis_files = list(self.data_dir.glob("brief_analysis_*.json"))
        if not analysis_files:
            return {"content": [{"type": "text", "text": "No brief analyses found"}]}
        
        # Load most recent analysis if no specific ID provided
        if not analysis_id:
            analysis_file = max(analysis_files, key=lambda x: x.stat().st_mtime)
        else:
            analysis_file = self.data_dir / f"brief_analysis_{analysis_id}.json"
            if not analysis_file.exists():
                return {"content": [{"type": "text", "text": f"Analysis {analysis_id} not found"}]}
        
        with open(analysis_file, 'r') as f:
            analysis = json.load(f)
        
        if requirement_type == "all":
            requirements = analysis['analysis']
        else:
            requirements = analysis['analysis'].get(requirement_type, {})
        
        result = f"""📋 **Requirements Extraction**

**Analysis:** {analysis_file.name}
**Type:** {requirement_type}

**Extracted Requirements:**
```json
{json.dumps(requirements, indent=2)}
```

**Summary:**
- Total requirement categories: {len(analysis['analysis'])}
- Questions for clarification: {len(analysis['questions_for_clarification'])}
- Risk factors: {len(analysis['risk_factors'])}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("client_communication", "Generate client communication or feedback response", {
        "communication_type": "str",
        "message_content": "str",
        "client_info": "dict"
    })
    async def client_communication(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate client communication or feedback response."""
        comm_type = args.get("communication_type", "general")
        message_content = args.get("message_content", "")
        client_info = args.get("client_info", {})
        
        client_name = client_info.get("name", "Valued Client")
        project_name = client_info.get("project_name", "your project")
        
        if comm_type == "brief_confirmation":
            response = f"""Dear {client_name},

Thank you for providing the brief for {project_name}. I've completed my analysis and have a few questions to ensure we deliver exactly what you need:

**Key Points I've Identified:**
- Your main business objectives
- Target audience characteristics  
- Key messages to communicate
- Deliverables and timeline

**Questions for Clarification:**
{message_content}

I'd like to schedule a brief call to discuss these points and ensure we're aligned before moving to the creative strategy phase.

Best regards,
Your Account Manager"""
        
        elif comm_type == "requirement_validation":
            response = f"""Hi {client_name},

I've extracted the key requirements from your brief for {project_name}. Here's what I understand:

**Project Requirements:**
{message_content}

**Next Steps:**
1. Please review and confirm these requirements
2. I'll hand this over to our Strategy Planner and Creative Director
3. We'll present the creative strategy within 3-5 business days

Does this accurately capture your vision?

Best,
Your Account Manager"""
        
        else:
            response = f"""Dear {client_name},

{message_content}

Please let me know if you have any questions or need clarification on any points.

Best regards,
Your Account Manager"""
        
        # Save communication
        comm_file = self.data_dir / f"client_communication_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        communication = {
            "timestamp": datetime.now().isoformat(),
            "client_info": client_info,
            "type": comm_type,
            "message": response,
            "original_content": message_content
        }
        
        with open(comm_file, 'w') as f:
            json.dump(communication, f, indent=2)
        
        return {"content": [{"type": "text", "text": response}]}
    
    @tool("validate_brief", "Validate brief completeness and identify missing information", {
        "brief_content": "str"
    })
    async def validate_brief(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Validate brief completeness and identify missing information."""
        brief_content = args.get("brief_content", "")
        
        if not brief_content:
            return {"content": [{"type": "text", "text": "Error: Brief content is required"}]}
        
        # Define required elements
        required_elements = {
            "business_objectives": ["goal", "objective", "purpose", "aim"],
            "target_audience": ["audience", "target", "demographic", "customer"],
            "budget": ["budget", "cost", "investment", "spend"],
            "timeline": ["timeline", "deadline", "schedule", "launch"],
            "deliverables": ["deliverable", "output", "asset", "material"],
            "brand_guidelines": ["brand", "logo", "style", "guideline"]
        }
        
        missing_elements = []
        present_elements = []
        
        brief_lower = brief_content.lower()
        
        for element, keywords in required_elements.items():
            if any(keyword in brief_lower for keyword in keywords):
                present_elements.append(element)
            else:
                missing_elements.append(element)
        
        completeness_score = len(present_elements) / len(required_elements) * 100
        
        result = f"""✅ **Brief Validation Complete**

**Completeness Score:** {completeness_score:.1f}%

**Present Elements:**
{chr(10).join(f"✅ {element}" for element in present_elements)}

**Missing Elements:**
{chr(10).join(f"❌ {element}" for element in missing_elements)}

**Recommendations:**
"""
        
        if missing_elements:
            result += f"- Request clarification on: {', '.join(missing_elements)}\n"
        
        if completeness_score >= 80:
            result += "- Brief is comprehensive and ready for analysis\n"
        elif completeness_score >= 60:
            result += "- Brief is good but needs some clarification\n"
        else:
            result += "- Brief needs significant additional information\n"
        
        result += f"- Schedule client call to address missing elements\n"
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("create_brief_summary", "Create executive summary of brief analysis", {
        "analysis_id": "str"
    })
    async def create_brief_summary(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create executive summary of brief analysis."""
        analysis_id = args.get("analysis_id", "")
        
        # Find analysis file
        analysis_files = list(self.data_dir.glob("brief_analysis_*.json"))
        if not analysis_files:
            return {"content": [{"type": "text", "text": "No brief analyses found"}]}
        
        # Load most recent analysis if no specific ID provided
        if not analysis_id:
            analysis_file = max(analysis_files, key=lambda x: x.stat().st_mtime)
        else:
            analysis_file = self.data_dir / f"brief_analysis_{analysis_id}.json"
            if not analysis_file.exists():
                return {"content": [{"type": "text", "text": f"Analysis {analysis_id} not found"}]}
        
        with open(analysis_file, 'r') as f:
            analysis = json.load(f)
        
        client_info = analysis.get("client_info", {})
        analysis_data = analysis.get("analysis", {})
        
        summary = f"""📊 **Executive Brief Summary**

**Client:** {client_info.get('name', 'Unknown')}
**Project:** {client_info.get('project_name', 'Unnamed Project')}
**Date:** {analysis.get('timestamp', 'Unknown')}

**Business Objectives:**
{chr(10).join(f"• {obj}" for obj in analysis_data.get('business_objectives', []))}

**Target Audience:**
{json.dumps(analysis_data.get('target_audience', {}), indent=2)}

**Key Messages:**
{chr(10).join(f"• {msg}" for msg in analysis_data.get('key_messages', []))}

**Deliverables:**
{chr(10).join(f"• {deliverable}" for deliverable in analysis_data.get('deliverables', []))}

**Constraints:**
- Budget: {analysis_data.get('constraints', {}).get('budget', 'Not specified')}
- Timeline: {analysis_data.get('constraints', {}).get('timeline', 'Not specified')}

**Success Metrics:**
{chr(10).join(f"• {metric}" for metric in analysis_data.get('success_metrics', []))}

**Questions for Clarification:**
{len(analysis.get('questions_for_clarification', []))} items identified

**Risk Factors:**
{len(analysis.get('risk_factors', []))} items identified

**Recommendations:**
{len(analysis.get('recommendations', []))} items provided

---
*Analysis completed by Account Manager Agent*"""
        
        return {"content": [{"type": "text", "text": summary}]}


async def main():
    """Main entry point for the Account Manager agent."""
    config_dir = Path("sub-agents/account-manager")
    agent = AccountManagerAgent(config_dir)
    
    print("🎯 Account Manager Agent")
    print("=" * 50)
    print("Welcome! I'm your AI Account Manager specializing in:")
    print("• Brief analysis and requirement extraction")
    print("• Client communication and relationship management")
    print("• Project scope definition and validation")
    print("• Stakeholder alignment and feedback")
    print()
    print("I work closely with Strategy Planner and Creative Director")
    print("to ensure your projects start with crystal-clear requirements.")
    print()
    
    async with agent:
        await agent.run_interactive()


if __name__ == "__main__":
    asyncio.run(main())

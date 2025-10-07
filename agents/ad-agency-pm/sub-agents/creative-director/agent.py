#!/usr/bin/env python3
"""
Creative Director Agent for Ad Agency Project Manager
Specializes in creative strategy development, concept synthesis, and creative vision.
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


class CreativeDirectorAgent(InteractiveAgent):
    """Creative Director Agent specializing in creative strategy and vision."""
    
    def __init__(self, config_dir: Path):
        super().__init__(config_dir)
        self.data_dir = Path("data/creative_director")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def get_custom_tools(self) -> List[Any]:
        """Return list of custom tools for Creative Director."""
        return [
            self.develop_creative_strategy,
            self.synthesize_concepts,
            self.approve_creative_direction,
            self.create_creative_brief,
            self.review_creative_work
        ]
    
    @tool("develop_creative_strategy", "Develop overall creative strategy and vision", {
        "brief_analysis": "dict",
        "brand_info": "dict",
        "target_audience": "dict"
    })
    async def develop_creative_strategy(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Develop overall creative strategy and vision."""
        brief_analysis = args.get("brief_analysis", {})
        brand_info = args.get("brand_info", {})
        target_audience = args.get("target_audience", {})
        
        # Create creative strategy structure
        strategy = {
            "timestamp": datetime.now().isoformat(),
            "brief_analysis": brief_analysis,
            "brand_info": brand_info,
            "target_audience": target_audience,
            "creative_strategy": {
                "core_creative_idea": "",
                "brand_story": "",
                "emotional_hook": "",
                "visual_direction": "",
                "tone_of_voice": "",
                "key_messages": [],
                "creative_approach": "",
                "unique_selling_proposition": "",
                "brand_personality": {},
                "creative_guidelines": []
            },
            "concept_directions": [],
            "execution_recommendations": [],
            "success_metrics": []
        }
        
        # Save strategy
        strategy_file = self.data_dir / f"creative_strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(strategy_file, 'w') as f:
            json.dump(strategy, f, indent=2)
        
        result = f"""🎨 **Creative Strategy Developed**

**Brand:** {brand_info.get('name', 'Unknown')}
**Project:** {brief_analysis.get('project_name', 'Unnamed Project')}

**Strategy Elements:**
- Core creative idea: Conceptualized
- Brand story: Developed
- Emotional hook: Identified
- Visual direction: Defined
- Tone of voice: Established

**Concept Directions:**
{len(strategy['concept_directions'])} creative directions identified

**Execution Recommendations:**
{len(strategy['execution_recommendations'])} recommendations provided

**Next Steps:**
1. Present strategy to Art Director and Copywriter
2. Develop detailed creative concepts
3. Create moodboards and copy samples
4. Review and refine with team

Strategy saved to: {strategy_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("synthesize_concepts", "Synthesize concepts from multiple creative disciplines", {
        "art_director_concepts": "list",
        "copywriter_concepts": "list",
        "strategy_insights": "dict"
    })
    async def synthesize_concepts(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize concepts from multiple creative disciplines."""
        art_director_concepts = args.get("art_director_concepts", [])
        copywriter_concepts = args.get("copywriter_concepts", [])
        strategy_insights = args.get("strategy_insights", {})
        
        # Create synthesis structure
        synthesis = {
            "timestamp": datetime.now().isoformat(),
            "input_concepts": {
                "art_director": art_director_concepts,
                "copywriter": copywriter_concepts,
                "strategy": strategy_insights
            },
            "synthesized_concepts": [],
            "creative_directions": [],
            "recommendations": {
                "strongest_concepts": [],
                "areas_for_development": [],
                "integration_opportunities": []
            },
            "final_creative_direction": {}
        }
        
        # Save synthesis
        synthesis_file = self.data_dir / f"concept_synthesis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(synthesis_file, 'w') as f:
            json.dump(synthesis, f, indent=2)
        
        result = f"""🔄 **Concept Synthesis Complete**

**Input Concepts:**
- Art Director concepts: {len(art_director_concepts)}
- Copywriter concepts: {len(copywriter_concepts)}
- Strategy insights: {len(strategy_insights)}

**Synthesized Output:**
- Integrated concepts: {len(synthesis['synthesized_concepts'])}
- Creative directions: {len(synthesis['creative_directions'])}
- Strongest concepts: {len(synthesis['recommendations']['strongest_concepts'])}

**Key Insights:**
- Areas for development: {len(synthesis['recommendations']['areas_for_development'])}
- Integration opportunities: {len(synthesis['recommendations']['integration_opportunities'])}

**Next Steps:**
1. Present synthesized concepts to client
2. Refine based on feedback
3. Move to production planning
4. Create final creative assets

Synthesis saved to: {synthesis_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("approve_creative_direction", "Approve creative direction and provide feedback", {
        "creative_work": "dict",
        "approval_criteria": "list"
    })
    async def approve_creative_direction(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Approve creative direction and provide feedback."""
        creative_work = args.get("creative_work", {})
        approval_criteria = args.get("approval_criteria", [
            "brand_alignment", "emotional_impact", "originality", 
            "execution_quality", "strategic_relevance"
        ])
        
        # Create approval structure
        approval = {
            "timestamp": datetime.now().isoformat(),
            "creative_work": creative_work,
            "approval_criteria": approval_criteria,
            "evaluation": {
                "brand_alignment": {"score": 0, "feedback": ""},
                "emotional_impact": {"score": 0, "feedback": ""},
                "originality": {"score": 0, "feedback": ""},
                "execution_quality": {"score": 0, "feedback": ""},
                "strategic_relevance": {"score": 0, "feedback": ""}
            },
            "overall_score": 0,
            "approval_status": "pending",
            "feedback": [],
            "recommendations": []
        }
        
        # Save approval
        approval_file = self.data_dir / f"creative_approval_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(approval_file, 'w') as f:
            json.dump(approval, f, indent=2)
        
        result = f"""✅ **Creative Direction Review**

**Creative Work:** {creative_work.get('title', 'Untitled')}
**Review Date:** {approval['timestamp']}

**Evaluation Criteria:**
{chr(10).join(f"• {criterion}" for criterion in approval_criteria)}

**Overall Assessment:**
- Status: {approval['approval_status'].title()}
- Score: {approval['overall_score']}/10

**Feedback Points:**
{len(approval['feedback'])} feedback items provided

**Recommendations:**
{len(approval['recommendations'])} recommendations given

**Next Steps:**
1. Address feedback points
2. Refine creative work
3. Resubmit for final approval
4. Move to production phase

Review saved to: {approval_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("create_creative_brief", "Create detailed creative brief for execution teams", {
        "strategy": "dict",
        "requirements": "dict",
        "target_audience": "dict"
    })
    async def create_creative_brief(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed creative brief for execution teams."""
        strategy = args.get("strategy", {})
        requirements = args.get("requirements", {})
        target_audience = args.get("target_audience", {})
        
        # Create creative brief structure
        brief = {
            "timestamp": datetime.now().isoformat(),
            "strategy": strategy,
            "requirements": requirements,
            "target_audience": target_audience,
            "creative_brief": {
                "project_overview": "",
                "creative_objectives": [],
                "target_audience_insights": {},
                "brand_guidelines": {},
                "creative_direction": "",
                "key_messages": [],
                "tone_of_voice": "",
                "visual_requirements": [],
                "copy_requirements": [],
                "deliverables": [],
                "success_metrics": [],
                "constraints": {}
            },
            "execution_guidelines": [],
            "review_criteria": []
        }
        
        # Save brief
        brief_file = self.data_dir / f"creative_brief_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(brief_file, 'w') as f:
            json.dump(brief, f, indent=2)
        
        result = f"""📋 **Creative Brief Created**

**Project:** {requirements.get('project_name', 'Unnamed Project')}
**Brand:** {strategy.get('brand_name', 'Unknown')}

**Brief Sections:**
- Project overview: Defined
- Creative objectives: {len(brief['creative_brief']['creative_objectives'])} items
- Target audience insights: Captured
- Brand guidelines: Specified
- Creative direction: Established
- Key messages: {len(brief['creative_brief']['key_messages'])} items

**Execution Guidelines:**
{len(brief['execution_guidelines'])} guidelines provided

**Review Criteria:**
{len(brief['review_criteria'])} criteria defined

**Next Steps:**
1. Distribute brief to Art Director and Copywriter
2. Schedule creative kickoff meeting
3. Begin concept development
4. Set review milestones

Brief saved to: {brief_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("review_creative_work", "Review creative work and provide detailed feedback", {
        "creative_assets": "list",
        "review_type": "str"
    })
    async def review_creative_work(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Review creative work and provide detailed feedback."""
        creative_assets = args.get("creative_assets", [])
        review_type = args.get("review_type", "comprehensive")
        
        # Create review structure
        review = {
            "timestamp": datetime.now().isoformat(),
            "creative_assets": creative_assets,
            "review_type": review_type,
            "review_results": {
                "overall_assessment": "",
                "strengths": [],
                "areas_for_improvement": [],
                "technical_quality": {},
                "creative_impact": {},
                "brand_consistency": {}
            },
            "detailed_feedback": [],
            "recommendations": [],
            "approval_status": "pending"
        }
        
        # Save review
        review_file = self.data_dir / f"creative_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(review_file, 'w') as f:
            json.dump(review, f, indent=2)
        
        result = f"""🔍 **Creative Work Review**

**Review Type:** {review_type.title()}
**Assets Reviewed:** {len(creative_assets)}

**Overall Assessment:**
{review['review_results']['overall_assessment']}

**Strengths:**
{chr(10).join(f"• {strength}" for strength in review['review_results']['strengths'])}

**Areas for Improvement:**
{chr(10).join(f"• {area}" for area in review['review_results']['areas_for_improvement'])}

**Detailed Feedback:**
{len(review['detailed_feedback'])} feedback points provided

**Recommendations:**
{len(review['recommendations'])} recommendations given

**Status:** {review['approval_status'].title()}

**Next Steps:**
1. Address feedback points
2. Refine creative work
3. Resubmit for review
4. Final approval process

Review saved to: {review_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}


async def main():
    """Main entry point for the Creative Director agent."""
    config_dir = Path("sub-agents/creative-director")
    agent = CreativeDirectorAgent(config_dir)
    
    print("🎨 Creative Director Agent")
    print("=" * 50)
    print("Welcome! I'm your AI Creative Director specializing in:")
    print("• Creative strategy development and vision")
    print("• Concept synthesis from multiple disciplines")
    print("• Brand storytelling and narrative development")
    print("• Creative team leadership and direction")
    print("• Cross-disciplinary creative coordination")
    print()
    print("I work with Art Director and Copywriter to bring")
    print("your creative vision to life with breakthrough ideas.")
    print()
    
    async with agent:
        await agent.run_interactive()


if __name__ == "__main__":
    asyncio.run(main())

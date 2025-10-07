#!/usr/bin/env python3
"""
Art Director Agent for Ad Agency Project Manager
Specializes in visual concept development, design direction, and visual asset creation.
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


class ArtDirectorAgent(InteractiveAgent):
    """Art Director Agent specializing in visual concepts and design direction."""
    
    def __init__(self, config_dir: Path):
        super().__init__(config_dir)
        self.data_dir = Path("data/art_director")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def get_custom_tools(self) -> List[Any]:
        """Return list of custom tools for Art Director."""
        return [
            self.create_visual_concept,
            self.design_moodboard,
            self.review_visual_assets,
            self.create_design_specifications,
            self.develop_visual_guidelines
        ]
    
    @tool("create_visual_concept", "Create visual concept and design direction", {
        "creative_brief": "dict",
        "brand_guidelines": "dict",
        "target_audience": "dict"
    })
    async def create_visual_concept(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create visual concept and design direction."""
        creative_brief = args.get("creative_brief", {})
        brand_guidelines = args.get("brand_guidelines", {})
        target_audience = args.get("target_audience", {})
        
        # Create visual concept structure
        concept = {
            "timestamp": datetime.now().isoformat(),
            "creative_brief": creative_brief,
            "brand_guidelines": brand_guidelines,
            "target_audience": target_audience,
            "visual_concept": {
                "core_visual_idea": "",
                "visual_style": "",
                "color_palette": [],
                "typography_choices": [],
                "imagery_style": "",
                "composition_approach": "",
                "visual_hierarchy": {},
                "emotional_tone": "",
                "brand_consistency": {},
                "cross_platform_adaptation": {}
            },
            "design_directions": [],
            "visual_references": [],
            "technical_requirements": []
        }
        
        # Save concept
        concept_file = self.data_dir / f"visual_concept_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(concept_file, 'w') as f:
            json.dump(concept, f, indent=2)
        
        result = f"""🎨 **Visual Concept Created**

**Project:** {creative_brief.get('project_name', 'Unnamed Project')}
**Brand:** {brand_guidelines.get('brand_name', 'Unknown')}

**Visual Concept Elements:**
- Core visual idea: Conceptualized
- Visual style: Defined
- Color palette: {len(concept['visual_concept']['color_palette'])} colors
- Typography choices: {len(concept['visual_concept']['typography_choices'])} fonts
- Imagery style: Established
- Composition approach: Defined

**Design Directions:**
{len(concept['design_directions'])} visual directions developed

**Visual References:**
{len(concept['visual_references'])} reference materials identified

**Technical Requirements:**
{len(concept['technical_requirements'])} technical specs defined

**Next Steps:**
1. Create detailed moodboard
2. Develop design specifications
3. Collaborate with Copywriter on integration
4. Present to Creative Director for approval

Concept saved to: {concept_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("design_moodboard", "Create visual moodboard with references and inspiration", {
        "visual_concept": "dict",
        "style_keywords": "list"
    })
    async def design_moodboard(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create visual moodboard with references and inspiration."""
        visual_concept = args.get("visual_concept", {})
        style_keywords = args.get("style_keywords", [])
        
        # Create moodboard structure
        moodboard = {
            "timestamp": datetime.now().isoformat(),
            "visual_concept": visual_concept,
            "style_keywords": style_keywords,
            "moodboard": {
                "color_inspiration": [],
                "typography_examples": [],
                "imagery_style": [],
                "composition_references": [],
                "texture_materials": [],
                "lighting_mood": [],
                "visual_metaphors": [],
                "brand_consistency_elements": []
            },
            "reference_categories": {
                "contemporary": [],
                "classic": [],
                "innovative": [],
                "brand_aligned": []
            },
            "visual_narrative": "",
            "implementation_notes": []
        }
        
        # Save moodboard
        moodboard_file = self.data_dir / f"moodboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(moodboard_file, 'w') as f:
            json.dump(moodboard, f, indent=2)
        
        result = f"""🖼️ **Visual Moodboard Created**

**Style Keywords:** {', '.join(style_keywords)}
**Visual Concept:** {visual_concept.get('core_visual_idea', 'Not specified')}

**Moodboard Elements:**
- Color inspiration: {len(moodboard['moodboard']['color_inspiration'])} references
- Typography examples: {len(moodboard['moodboard']['typography_examples'])} samples
- Imagery style: {len(moodboard['moodboard']['imagery_style'])} references
- Composition references: {len(moodboard['moodboard']['composition_references'])} examples
- Texture materials: {len(moodboard['moodboard']['texture_materials'])} samples
- Lighting mood: {len(moodboard['moodboard']['lighting_mood'])} references

**Reference Categories:**
- Contemporary: {len(moodboard['reference_categories']['contemporary'])} items
- Classic: {len(moodboard['reference_categories']['classic'])} items
- Innovative: {len(moodboard['reference_categories']['innovative'])} items
- Brand aligned: {len(moodboard['reference_categories']['brand_aligned'])} items

**Visual Narrative:**
{moodboard['visual_narrative']}

**Implementation Notes:**
{len(moodboard['implementation_notes'])} notes provided

**Next Steps:**
1. Present moodboard to Creative Director
2. Refine based on feedback
3. Create detailed design specifications
4. Begin asset creation

Moodboard saved to: {moodboard_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("review_visual_assets", "Review visual assets and provide design feedback", {
        "visual_assets": "list",
        "review_criteria": "list"
    })
    async def review_visual_assets(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Review visual assets and provide design feedback."""
        visual_assets = args.get("visual_assets", [])
        review_criteria = args.get("review_criteria", [
            "visual_impact", "brand_consistency", "composition", 
            "color_usage", "typography", "technical_quality"
        ])
        
        # Create review structure
        review = {
            "timestamp": datetime.now().isoformat(),
            "visual_assets": visual_assets,
            "review_criteria": review_criteria,
            "review_results": {
                "overall_assessment": "",
                "visual_impact_score": 0,
                "brand_consistency_score": 0,
                "composition_score": 0,
                "color_usage_score": 0,
                "typography_score": 0,
                "technical_quality_score": 0
            },
            "detailed_feedback": [],
            "strengths": [],
            "areas_for_improvement": [],
            "recommendations": [],
            "approval_status": "pending"
        }
        
        # Save review
        review_file = self.data_dir / f"visual_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(review_file, 'w') as f:
            json.dump(review, f, indent=2)
        
        result = f"""🔍 **Visual Assets Review**

**Assets Reviewed:** {len(visual_assets)}
**Review Criteria:** {', '.join(review_criteria)}

**Overall Assessment:**
{review['review_results']['overall_assessment']}

**Scores:**
- Visual Impact: {review['review_results']['visual_impact_score']}/10
- Brand Consistency: {review['review_results']['brand_consistency_score']}/10
- Composition: {review['review_results']['composition_score']}/10
- Color Usage: {review['review_results']['color_usage_score']}/10
- Typography: {review['review_results']['typography_score']}/10
- Technical Quality: {review['review_results']['technical_quality_score']}/10

**Strengths:**
{chr(10).join(f"• {strength}" for strength in review['strengths'])}

**Areas for Improvement:**
{chr(10).join(f"• {area}" for area in review['areas_for_improvement'])}

**Detailed Feedback:**
{len(review['detailed_feedback'])} feedback points provided

**Recommendations:**
{len(review['recommendations'])} recommendations given

**Status:** {review['approval_status'].title()}

**Next Steps:**
1. Address feedback points
2. Refine visual assets
3. Resubmit for review
4. Final approval process

Review saved to: {review_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("create_design_specifications", "Create detailed design specifications for production", {
        "visual_concept": "dict",
        "deliverables": "list"
    })
    async def create_design_specifications(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed design specifications for production."""
        visual_concept = args.get("visual_concept", {})
        deliverables = args.get("deliverables", [])
        
        # Create specifications structure
        specifications = {
            "timestamp": datetime.now().isoformat(),
            "visual_concept": visual_concept,
            "deliverables": deliverables,
            "design_specifications": {
                "color_specifications": {},
                "typography_specifications": {},
                "imagery_requirements": {},
                "layout_guidelines": {},
                "technical_requirements": {},
                "file_formats": {},
                "resolution_requirements": {},
                "brand_guidelines_compliance": {}
            },
            "production_notes": [],
            "quality_checklist": [],
            "delivery_requirements": []
        }
        
        # Save specifications
        specs_file = self.data_dir / f"design_specifications_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(specs_file, 'w') as f:
            json.dump(specifications, f, indent=2)
        
        result = f"""📐 **Design Specifications Created**

**Project:** {visual_concept.get('project_name', 'Unnamed Project')}
**Deliverables:** {len(deliverables)} items

**Specification Categories:**
- Color specifications: Defined
- Typography specifications: Established
- Imagery requirements: Specified
- Layout guidelines: Created
- Technical requirements: Detailed
- File formats: Specified
- Resolution requirements: Defined
- Brand guidelines compliance: Verified

**Production Notes:**
{len(specifications['production_notes'])} notes provided

**Quality Checklist:**
{len(specifications['quality_checklist'])} checkpoints defined

**Delivery Requirements:**
{len(specifications['delivery_requirements'])} requirements specified

**Next Steps:**
1. Distribute specifications to production team
2. Begin asset creation process
3. Implement quality checkpoints
4. Prepare for delivery

Specifications saved to: {specs_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("develop_visual_guidelines", "Develop comprehensive visual brand guidelines", {
        "brand_info": "dict",
        "visual_concept": "dict"
    })
    async def develop_visual_guidelines(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Develop comprehensive visual brand guidelines."""
        brand_info = args.get("brand_info", {})
        visual_concept = args.get("visual_concept", {})
        
        # Create guidelines structure
        guidelines = {
            "timestamp": datetime.now().isoformat(),
            "brand_info": brand_info,
            "visual_concept": visual_concept,
            "visual_guidelines": {
                "logo_usage": {},
                "color_palette": {},
                "typography_system": {},
                "imagery_style": {},
                "layout_principles": {},
                "spacing_system": {},
                "iconography": {},
                "do_and_dont_examples": {}
            },
            "application_examples": [],
            "cross_platform_adaptations": {},
            "brand_consistency_rules": []
        }
        
        # Save guidelines
        guidelines_file = self.data_dir / f"visual_guidelines_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(guidelines_file, 'w') as f:
            json.dump(guidelines, f, indent=2)
        
        result = f"""📋 **Visual Brand Guidelines Developed**

**Brand:** {brand_info.get('name', 'Unknown')}
**Project:** {visual_concept.get('project_name', 'Unnamed Project')}

**Guideline Sections:**
- Logo usage: Defined
- Color palette: Established
- Typography system: Created
- Imagery style: Specified
- Layout principles: Defined
- Spacing system: Established
- Iconography: Created
- Do and don't examples: Provided

**Application Examples:**
{len(guidelines['application_examples'])} examples provided

**Cross-Platform Adaptations:**
{len(guidelines['cross_platform_adaptations'])} adaptations defined

**Brand Consistency Rules:**
{len(guidelines['brand_consistency_rules'])} rules established

**Next Steps:**
1. Present guidelines to Creative Director
2. Distribute to all creative teams
3. Implement in current project
4. Use for future brand consistency

Guidelines saved to: {guidelines_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}


async def main():
    """Main entry point for the Art Director agent."""
    config_dir = Path("sub-agents/art-director")
    agent = ArtDirectorAgent(config_dir)
    
    print("🎨 Art Director Agent")
    print("=" * 50)
    print("Welcome! I'm your AI Art Director specializing in:")
    print("• Visual concept development and design direction")
    print("• Moodboard creation and visual references")
    print("• Visual asset review and feedback")
    print("• Design specifications and production guidance")
    print("• Visual brand guidelines development")
    print()
    print("I work with Creative Director and Copywriter to create")
    print("visually stunning and brand-consistent creative work.")
    print()
    
    async with agent:
        await agent.run_interactive()


if __name__ == "__main__":
    asyncio.run(main())

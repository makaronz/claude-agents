#!/usr/bin/env python3
"""
Copywriter Agent for Ad Agency Project Manager
Specializes in messaging development, copy creation, and tone of voice.
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


class CopywriterAgent(InteractiveAgent):
    """Copywriter Agent specializing in messaging and copy creation."""
    
    def __init__(self, config_dir: Path):
        super().__init__(config_dir)
        self.data_dir = Path("data/copywriter")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def get_custom_tools(self) -> List[Any]:
        """Return list of custom tools for Copywriter."""
        return [
            self.develop_messaging,
            self.write_copy,
            self.create_tone_of_voice,
            self.review_copy,
            self.adapt_copy_for_platforms
        ]
    
    @tool("develop_messaging", "Develop strategic messaging framework and key messages", {
        "creative_brief": "dict",
        "target_audience": "dict",
        "brand_voice": "dict"
    })
    async def develop_messaging(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Develop strategic messaging framework and key messages."""
        creative_brief = args.get("creative_brief", {})
        target_audience = args.get("target_audience", {})
        brand_voice = args.get("brand_voice", {})
        
        # Create messaging structure
        messaging = {
            "timestamp": datetime.now().isoformat(),
            "creative_brief": creative_brief,
            "target_audience": target_audience,
            "brand_voice": brand_voice,
            "messaging_framework": {
                "core_message": "",
                "key_messages": [],
                "supporting_messages": [],
                "emotional_hooks": [],
                "rational_benefits": [],
                "unique_selling_propositions": [],
                "call_to_actions": [],
                "messaging_hierarchy": {}
            },
            "tone_guidelines": {},
            "language_preferences": {},
            "audience_specific_messaging": {}
        }
        
        # Save messaging
        messaging_file = self.data_dir / f"messaging_framework_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(messaging_file, 'w') as f:
            json.dump(messaging, f, indent=2)
        
        result = f"""✍️ **Messaging Framework Developed**

**Project:** {creative_brief.get('project_name', 'Unnamed Project')}
**Target Audience:** {target_audience.get('primary', 'Not specified')}

**Messaging Elements:**
- Core message: Defined
- Key messages: {len(messaging['messaging_framework']['key_messages'])} items
- Supporting messages: {len(messaging['messaging_framework']['supporting_messages'])} items
- Emotional hooks: {len(messaging['messaging_framework']['emotional_hooks'])} hooks
- Rational benefits: {len(messaging['messaging_framework']['rational_benefits'])} benefits
- USPs: {len(messaging['messaging_framework']['unique_selling_propositions'])} propositions
- CTAs: {len(messaging['messaging_framework']['call_to_actions'])} actions

**Tone Guidelines:**
{len(messaging['tone_guidelines'])} tone specifications

**Language Preferences:**
{len(messaging['language_preferences'])} language guidelines

**Audience-Specific Messaging:**
{len(messaging['audience_specific_messaging'])} audience variations

**Next Steps:**
1. Create specific copy for different touchpoints
2. Develop tone of voice guidelines
3. Collaborate with Art Director on integration
4. Present to Creative Director for approval

Messaging saved to: {messaging_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("write_copy", "Write compelling copy for specific touchpoints and media", {
        "messaging_framework": "dict",
        "touchpoint": "str",
        "media_type": "str",
        "character_limit": "int"
    })
    async def write_copy(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Write compelling copy for specific touchpoints and media."""
        messaging_framework = args.get("messaging_framework", {})
        touchpoint = args.get("touchpoint", "general")
        media_type = args.get("media_type", "digital")
        character_limit = args.get("character_limit", 0)
        
        # Create copy structure
        copy_work = {
            "timestamp": datetime.now().isoformat(),
            "messaging_framework": messaging_framework,
            "touchpoint": touchpoint,
            "media_type": media_type,
            "character_limit": character_limit,
            "copy_variations": {
                "headline": "",
                "subheadline": "",
                "body_copy": "",
                "call_to_action": "",
                "tagline": "",
                "social_media_copy": "",
                "email_subject": "",
                "meta_description": ""
            },
            "tone_application": {},
            "audience_adaptation": {},
            "platform_optimization": {}
        }
        
        # Save copy
        copy_file = self.data_dir / f"copy_{touchpoint}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(copy_file, 'w') as f:
            json.dump(copy_work, f, indent=2)
        
        result = f"""📝 **Copy Created**

**Touchpoint:** {touchpoint.title()}
**Media Type:** {media_type.title()}
**Character Limit:** {character_limit if character_limit > 0 else 'No limit'}

**Copy Elements:**
- Headline: Created
- Subheadline: Written
- Body copy: Developed
- Call to action: Crafted
- Tagline: Created
- Social media copy: Written
- Email subject: Crafted
- Meta description: Created

**Tone Application:**
{len(copy_work['tone_application'])} tone applications

**Audience Adaptation:**
{len(copy_work['audience_adaptation'])} adaptations

**Platform Optimization:**
{len(copy_work['platform_optimization'])} optimizations

**Next Steps:**
1. Review copy with Creative Director
2. Test with target audience
3. Refine based on feedback
4. Finalize for production

Copy saved to: {copy_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("create_tone_of_voice", "Create comprehensive tone of voice guidelines", {
        "brand_personality": "dict",
        "target_audience": "dict",
        "messaging_framework": "dict"
    })
    async def create_tone_of_voice(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive tone of voice guidelines."""
        brand_personality = args.get("brand_personality", {})
        target_audience = args.get("target_audience", {})
        messaging_framework = args.get("messaging_framework", {})
        
        # Create tone of voice structure
        tone_of_voice = {
            "timestamp": datetime.now().isoformat(),
            "brand_personality": brand_personality,
            "target_audience": target_audience,
            "messaging_framework": messaging_framework,
            "tone_guidelines": {
                "overall_tone": "",
                "personality_traits": [],
                "voice_characteristics": {},
                "language_style": {},
                "emotional_tone": {},
                "communication_style": {}
            },
            "do_and_dont_examples": {
                "do_examples": [],
                "dont_examples": []
            },
            "platform_specific_adaptations": {},
            "audience_specific_variations": {},
            "brand_consistency_rules": []
        }
        
        # Save tone of voice
        tone_file = self.data_dir / f"tone_of_voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(tone_file, 'w') as f:
            json.dump(tone_of_voice, f, indent=2)
        
        result = f"""🎭 **Tone of Voice Guidelines Created**

**Brand:** {brand_personality.get('name', 'Unknown')}
**Target Audience:** {target_audience.get('primary', 'Not specified')}

**Tone Guidelines:**
- Overall tone: Defined
- Personality traits: {len(tone_of_voice['tone_guidelines']['personality_traits'])} traits
- Voice characteristics: Specified
- Language style: Established
- Emotional tone: Defined
- Communication style: Specified

**Do and Don't Examples:**
- Do examples: {len(tone_of_voice['do_and_dont_examples']['do_examples'])} examples
- Don't examples: {len(tone_of_voice['do_and_dont_examples']['dont_examples'])} examples

**Platform-Specific Adaptations:**
{len(tone_of_voice['platform_specific_adaptations'])} adaptations

**Audience-Specific Variations:**
{len(tone_of_voice['audience_specific_variations'])} variations

**Brand Consistency Rules:**
{len(tone_of_voice['brand_consistency_rules'])} rules

**Next Steps:**
1. Distribute guidelines to all copywriters
2. Implement in current project
3. Train team on tone application
4. Use for future brand consistency

Tone of voice saved to: {tone_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("review_copy", "Review copy and provide detailed feedback", {
        "copy_content": "dict",
        "review_criteria": "list"
    })
    async def review_copy(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Review copy and provide detailed feedback."""
        copy_content = args.get("copy_content", {})
        review_criteria = args.get("review_criteria", [
            "clarity", "persuasiveness", "brand_consistency", 
            "tone_accuracy", "call_to_action", "audience_appropriateness"
        ])
        
        # Create review structure
        review = {
            "timestamp": datetime.now().isoformat(),
            "copy_content": copy_content,
            "review_criteria": review_criteria,
            "review_results": {
                "overall_assessment": "",
                "clarity_score": 0,
                "persuasiveness_score": 0,
                "brand_consistency_score": 0,
                "tone_accuracy_score": 0,
                "call_to_action_score": 0,
                "audience_appropriateness_score": 0
            },
            "detailed_feedback": [],
            "strengths": [],
            "areas_for_improvement": [],
            "suggestions": [],
            "approval_status": "pending"
        }
        
        # Save review
        review_file = self.data_dir / f"copy_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(review_file, 'w') as f:
            json.dump(review, f, indent=2)
        
        result = f"""🔍 **Copy Review Complete**

**Copy Type:** {copy_content.get('type', 'General')}
**Review Criteria:** {', '.join(review_criteria)}

**Overall Assessment:**
{review['review_results']['overall_assessment']}

**Scores:**
- Clarity: {review['review_results']['clarity_score']}/10
- Persuasiveness: {review['review_results']['persuasiveness_score']}/10
- Brand Consistency: {review['review_results']['brand_consistency_score']}/10
- Tone Accuracy: {review['review_results']['tone_accuracy_score']}/10
- Call to Action: {review['review_results']['call_to_action_score']}/10
- Audience Appropriateness: {review['review_results']['audience_appropriateness_score']}/10

**Strengths:**
{chr(10).join(f"• {strength}" for strength in review['strengths'])}

**Areas for Improvement:**
{chr(10).join(f"• {area}" for area in review['areas_for_improvement'])}

**Detailed Feedback:**
{len(review['detailed_feedback'])} feedback points provided

**Suggestions:**
{len(review['suggestions'])} suggestions given

**Status:** {review['approval_status'].title()}

**Next Steps:**
1. Address feedback points
2. Refine copy based on suggestions
3. Resubmit for review
4. Final approval process

Review saved to: {review_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("adapt_copy_for_platforms", "Adapt copy for different platforms and media types", {
        "base_copy": "dict",
        "target_platforms": "list"
    })
    async def adapt_copy_for_platforms(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Adapt copy for different platforms and media types."""
        base_copy = args.get("base_copy", {})
        target_platforms = args.get("target_platforms", [])
        
        # Create adaptation structure
        adaptations = {
            "timestamp": datetime.now().isoformat(),
            "base_copy": base_copy,
            "target_platforms": target_platforms,
            "platform_adaptations": {},
            "optimization_notes": {},
            "character_limits": {},
            "platform_specific_guidelines": {}
        }
        
        # Create adaptations for each platform
        for platform in target_platforms:
            adaptations["platform_adaptations"][platform] = {
                "headline": "",
                "body_copy": "",
                "call_to_action": "",
                "hashtags": [],
                "mentions": []
            }
        
        # Save adaptations
        adaptations_file = self.data_dir / f"platform_adaptations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(adaptations_file, 'w') as f:
            json.dump(adaptations, f, indent=2)
        
        result = f"""📱 **Copy Adapted for Platforms**

**Base Copy:** {base_copy.get('type', 'General')}
**Target Platforms:** {', '.join(target_platforms)}

**Platform Adaptations:**
{chr(10).join(f"• {platform.title()}: Adapted" for platform in target_platforms)}

**Optimization Notes:**
{len(adaptations['optimization_notes'])} optimization notes

**Character Limits:**
{len(adaptations['character_limits'])} platform limits defined

**Platform-Specific Guidelines:**
{len(adaptations['platform_specific_guidelines'])} guidelines provided

**Next Steps:**
1. Review platform adaptations
2. Test with platform-specific audiences
3. Refine based on performance
4. Implement across all touchpoints

Adaptations saved to: {adaptations_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}


async def main():
    """Main entry point for the Copywriter agent."""
    config_dir = Path("sub-agents/copywriter")
    agent = CopywriterAgent(config_dir)
    
    print("✍️ Copywriter Agent")
    print("=" * 50)
    print("Welcome! I'm your AI Copywriter specializing in:")
    print("• Strategic messaging development and copy strategies")
    print("• Persuasive copywriting and storytelling")
    print("• Brand voice and tone development")
    print("• Cross-platform copy adaptation")
    print("• Emotional connection through words")
    print()
    print("I work with Creative Director and Art Director to create")
    print("compelling messages that connect with your audience.")
    print()
    
    async with agent:
        await agent.run_interactive()


if __name__ == "__main__":
    asyncio.run(main())

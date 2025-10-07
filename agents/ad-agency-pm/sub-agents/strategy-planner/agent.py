#!/usr/bin/env python3
"""
Strategy Planner Agent for Ad Agency Project Manager
Specializes in market analysis, target audience definition, and media strategy planning.
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


class StrategyPlannerAgent(InteractiveAgent):
    """Strategy Planner Agent specializing in market analysis and media planning."""
    
    def __init__(self, config_dir: Path):
        super().__init__(config_dir)
        self.data_dir = Path("data/strategy_planner")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def get_custom_tools(self) -> List[Any]:
        """Return list of custom tools for Strategy Planner."""
        return [
            self.analyze_market,
            self.define_target_audience,
            self.plan_media_strategy,
            self.create_insights_report,
            self.develop_campaign_strategy
        ]
    
    @tool("analyze_market", "Analyze market conditions and competitive landscape", {
        "industry": "str",
        "target_market": "str",
        "competitors": "list"
    })
    async def analyze_market(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market conditions and competitive landscape."""
        industry = args.get("industry", "")
        target_market = args.get("target_market", "")
        competitors = args.get("competitors", [])
        
        # Create market analysis structure
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "industry": industry,
            "target_market": target_market,
            "competitors": competitors,
            "market_analysis": {
                "market_size": {},
                "growth_trends": [],
                "key_drivers": [],
                "market_segments": [],
                "competitive_landscape": {},
                "opportunities": [],
                "threats": [],
                "market_timing": {}
            },
            "competitive_analysis": {
                "direct_competitors": [],
                "indirect_competitors": [],
                "competitive_positioning": {},
                "competitive_advantages": [],
                "market_gaps": []
            },
            "strategic_recommendations": []
        }
        
        # Save analysis
        analysis_file = self.data_dir / f"market_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        result = f"""📊 **Market Analysis Complete**

**Industry:** {industry}
**Target Market:** {target_market}
**Competitors Analyzed:** {len(competitors)}

**Market Analysis:**
- Market size: Analyzed
- Growth trends: {len(analysis['market_analysis']['growth_trends'])} trends identified
- Key drivers: {len(analysis['market_analysis']['key_drivers'])} drivers
- Market segments: {len(analysis['market_analysis']['market_segments'])} segments
- Opportunities: {len(analysis['market_analysis']['opportunities'])} opportunities
- Threats: {len(analysis['market_analysis']['threats'])} threats

**Competitive Analysis:**
- Direct competitors: {len(analysis['competitive_analysis']['direct_competitors'])} identified
- Indirect competitors: {len(analysis['competitive_analysis']['indirect_competitors'])} identified
- Competitive advantages: {len(analysis['competitive_analysis']['competitive_advantages'])} advantages
- Market gaps: {len(analysis['competitive_analysis']['market_gaps'])} gaps identified

**Strategic Recommendations:**
{len(analysis['strategic_recommendations'])} recommendations provided

**Next Steps:**
1. Define target audience based on market insights
2. Develop media strategy for identified opportunities
3. Create campaign strategy leveraging competitive advantages
4. Present findings to Creative Director

Analysis saved to: {analysis_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("define_target_audience", "Define target audience and create detailed personas", {
        "market_analysis": "dict",
        "brand_info": "dict",
        "campaign_objectives": "list"
    })
    async def define_target_audience(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Define target audience and create detailed personas."""
        market_analysis = args.get("market_analysis", {})
        brand_info = args.get("brand_info", {})
        campaign_objectives = args.get("campaign_objectives", [])
        
        # Create audience definition structure
        audience_definition = {
            "timestamp": datetime.now().isoformat(),
            "market_analysis": market_analysis,
            "brand_info": brand_info,
            "campaign_objectives": campaign_objectives,
            "target_audience": {
                "primary_audience": {},
                "secondary_audience": {},
                "audience_segments": [],
                "demographics": {},
                "psychographics": {},
                "behavioral_patterns": {},
                "media_consumption": {},
                "pain_points": [],
                "motivations": [],
                "influences": []
            },
            "personas": [],
            "audience_insights": [],
            "targeting_recommendations": []
        }
        
        # Save audience definition
        audience_file = self.data_dir / f"target_audience_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(audience_file, 'w') as f:
            json.dump(audience_definition, f, indent=2)
        
        result = f"""🎯 **Target Audience Defined**

**Brand:** {brand_info.get('name', 'Unknown')}
**Campaign Objectives:** {len(campaign_objectives)} objectives

**Audience Definition:**
- Primary audience: Defined
- Secondary audience: Identified
- Audience segments: {len(audience_definition['target_audience']['audience_segments'])} segments
- Demographics: Captured
- Psychographics: Analyzed
- Behavioral patterns: Identified
- Media consumption: Mapped
- Pain points: {len(audience_definition['target_audience']['pain_points'])} points
- Motivations: {len(audience_definition['target_audience']['motivations'])} motivations
- Influences: {len(audience_definition['target_audience']['influences'])} influences

**Personas Created:**
{len(audience_definition['personas'])} detailed personas

**Audience Insights:**
{len(audience_definition['audience_insights'])} key insights

**Targeting Recommendations:**
{len(audience_definition['targeting_recommendations'])} recommendations

**Next Steps:**
1. Plan media strategy based on audience media consumption
2. Develop creative strategy aligned with audience motivations
3. Create campaign strategy targeting identified segments
4. Present to Creative Director and Account Manager

Audience definition saved to: {audience_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("plan_media_strategy", "Plan comprehensive media strategy and channel selection", {
        "target_audience": "dict",
        "budget": "dict",
        "campaign_objectives": "list"
    })
    async def plan_media_strategy(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Plan comprehensive media strategy and channel selection."""
        target_audience = args.get("target_audience", {})
        budget = args.get("budget", {})
        campaign_objectives = args.get("campaign_objectives", [])
        
        # Create media strategy structure
        media_strategy = {
            "timestamp": datetime.now().isoformat(),
            "target_audience": target_audience,
            "budget": budget,
            "campaign_objectives": campaign_objectives,
            "media_strategy": {
                "channel_selection": [],
                "media_mix": {},
                "budget_allocation": {},
                "reach_and_frequency": {},
                "timing_strategy": {},
                "geographic_targeting": {},
                "audience_targeting": {}
            },
            "channel_recommendations": {
                "digital": [],
                "traditional": [],
                "social": [],
                "outdoor": [],
                "radio": [],
                "tv": []
            },
            "performance_metrics": [],
            "optimization_strategy": {}
        }
        
        # Save media strategy
        strategy_file = self.data_dir / f"media_strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(strategy_file, 'w') as f:
            json.dump(media_strategy, f, indent=2)
        
        result = f"""📺 **Media Strategy Planned**

**Budget:** {budget.get('total', 'Not specified')}
**Campaign Objectives:** {len(campaign_objectives)} objectives

**Media Strategy:**
- Channel selection: {len(media_strategy['media_strategy']['channel_selection'])} channels
- Media mix: Optimized
- Budget allocation: Planned
- Reach and frequency: Calculated
- Timing strategy: Defined
- Geographic targeting: Specified
- Audience targeting: Refined

**Channel Recommendations:**
- Digital: {len(media_strategy['channel_recommendations']['digital'])} channels
- Traditional: {len(media_strategy['channel_recommendations']['traditional'])} channels
- Social: {len(media_strategy['channel_recommendations']['social'])} platforms
- Outdoor: {len(media_strategy['channel_recommendations']['outdoor'])} formats
- Radio: {len(media_strategy['channel_recommendations']['radio'])} stations
- TV: {len(media_strategy['channel_recommendations']['tv'])} networks

**Performance Metrics:**
{len(media_strategy['performance_metrics'])} KPIs defined

**Optimization Strategy:**
{len(media_strategy['optimization_strategy'])} optimization tactics

**Next Steps:**
1. Present media strategy to Creative Director
2. Develop creative assets for selected channels
3. Create detailed media plan with Production Manager
4. Set up tracking and measurement systems

Media strategy saved to: {strategy_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("create_insights_report", "Create comprehensive insights report with strategic recommendations", {
        "market_analysis": "dict",
        "audience_analysis": "dict",
        "media_analysis": "dict"
    })
    async def create_insights_report(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive insights report with strategic recommendations."""
        market_analysis = args.get("market_analysis", {})
        audience_analysis = args.get("audience_analysis", {})
        media_analysis = args.get("media_analysis", {})
        
        # Create insights report structure
        insights_report = {
            "timestamp": datetime.now().isoformat(),
            "market_analysis": market_analysis,
            "audience_analysis": audience_analysis,
            "media_analysis": media_analysis,
            "executive_summary": "",
            "key_insights": [],
            "strategic_opportunities": [],
            "competitive_advantages": [],
            "audience_opportunities": [],
            "media_opportunities": [],
            "recommendations": {
                "immediate_actions": [],
                "short_term_strategy": [],
                "long_term_strategy": []
            },
            "success_metrics": [],
            "risk_assessment": []
        }
        
        # Save insights report
        report_file = self.data_dir / f"insights_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(insights_report, f, indent=2)
        
        result = f"""📈 **Insights Report Created**

**Analysis Components:**
- Market analysis: Completed
- Audience analysis: Completed
- Media analysis: Completed

**Report Sections:**
- Executive summary: Created
- Key insights: {len(insights_report['key_insights'])} insights
- Strategic opportunities: {len(insights_report['strategic_opportunities'])} opportunities
- Competitive advantages: {len(insights_report['competitive_advantages'])} advantages
- Audience opportunities: {len(insights_report['audience_opportunities'])} opportunities
- Media opportunities: {len(insights_report['media_opportunities'])} opportunities

**Recommendations:**
- Immediate actions: {len(insights_report['recommendations']['immediate_actions'])} actions
- Short-term strategy: {len(insights_report['recommendations']['short_term_strategy'])} strategies
- Long-term strategy: {len(insights_report['recommendations']['long_term_strategy'])} strategies

**Success Metrics:**
{len(insights_report['success_metrics'])} KPIs defined

**Risk Assessment:**
{len(insights_report['risk_assessment'])} risks identified

**Next Steps:**
1. Present insights to Creative Director and Account Manager
2. Develop campaign strategy based on recommendations
3. Create implementation plan with Production Manager
4. Set up measurement and tracking systems

Insights report saved to: {report_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("develop_campaign_strategy", "Develop comprehensive campaign strategy", {
        "insights_report": "dict",
        "creative_brief": "dict",
        "budget": "dict"
    })
    async def develop_campaign_strategy(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Develop comprehensive campaign strategy."""
        insights_report = args.get("insights_report", {})
        creative_brief = args.get("creative_brief", {})
        budget = args.get("budget", {})
        
        # Create campaign strategy structure
        campaign_strategy = {
            "timestamp": datetime.now().isoformat(),
            "insights_report": insights_report,
            "creative_brief": creative_brief,
            "budget": budget,
            "campaign_strategy": {
                "campaign_objectives": [],
                "target_audience": {},
                "key_messages": [],
                "media_strategy": {},
                "creative_strategy": {},
                "timeline": {},
                "budget_allocation": {},
                "success_metrics": []
            },
            "tactical_plan": {
                "phase_1": {},
                "phase_2": {},
                "phase_3": {}
            },
            "measurement_framework": {},
            "optimization_plan": {},
            "risk_mitigation": []
        }
        
        # Save campaign strategy
        strategy_file = self.data_dir / f"campaign_strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(strategy_file, 'w') as f:
            json.dump(campaign_strategy, f, indent=2)
        
        result = f"""🎯 **Campaign Strategy Developed**

**Project:** {creative_brief.get('project_name', 'Unnamed Project')}
**Budget:** {budget.get('total', 'Not specified')}

**Campaign Strategy:**
- Campaign objectives: {len(campaign_strategy['campaign_strategy']['campaign_objectives'])} objectives
- Target audience: Defined
- Key messages: {len(campaign_strategy['campaign_strategy']['key_messages'])} messages
- Media strategy: Planned
- Creative strategy: Outlined
- Timeline: Established
- Budget allocation: Optimized
- Success metrics: {len(campaign_strategy['campaign_strategy']['success_metrics'])} KPIs

**Tactical Plan:**
- Phase 1: Planned
- Phase 2: Outlined
- Phase 3: Conceptualized

**Measurement Framework:**
{len(campaign_strategy['measurement_framework'])} measurement components

**Optimization Plan:**
{len(campaign_strategy['optimization_plan'])} optimization tactics

**Risk Mitigation:**
{len(campaign_strategy['risk_mitigation'])} mitigation strategies

**Next Steps:**
1. Present strategy to Creative Director
2. Develop detailed creative brief
3. Create implementation plan with Production Manager
4. Begin campaign execution

Campaign strategy saved to: {strategy_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}


async def main():
    """Main entry point for the Strategy Planner agent."""
    config_dir = Path("sub-agents/strategy-planner")
    agent = StrategyPlannerAgent(config_dir)
    
    print("📊 Strategy Planner Agent")
    print("=" * 50)
    print("Welcome! I'm your AI Strategy Planner specializing in:")
    print("• Market research and competitive analysis")
    print("• Audience segmentation and persona development")
    print("• Media planning and channel optimization")
    print("• Data analysis and insights generation")
    print("• Strategic thinking and planning")
    print()
    print("I work with Creative Director and Account Manager to ensure")
    print("your campaigns are grounded in solid market insights.")
    print()
    
    async with agent:
        await agent.run_interactive()


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Production Manager Agent for Ad Agency Project Manager
Specializes in project timeline management, resource allocation, and production coordination.
"""

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

# Add parent directories to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from shared.agents import InteractiveAgent
from claude_agent_sdk import tool


class ProductionManagerAgent(InteractiveAgent):
    """Production Manager Agent specializing in project management and production coordination."""
    
    def __init__(self, config_dir: Path):
        super().__init__(config_dir)
        self.data_dir = Path("data/production_manager")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def get_custom_tools(self) -> List[Any]:
        """Return list of custom tools for Production Manager."""
        return [
            self.create_timeline,
            self.allocate_resources,
            self.track_production,
            self.manage_vendors,
            self.coordinate_deliverables
        ]
    
    @tool("create_timeline", "Create detailed project timeline and schedule", {
        "project_scope": "dict",
        "deliverables": "list",
        "deadline": "str",
        "team_availability": "dict"
    })
    async def create_timeline(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed project timeline and schedule."""
        project_scope = args.get("project_scope", {})
        deliverables = args.get("deliverables", [])
        deadline = args.get("deadline", "")
        team_availability = args.get("team_availability", {})
        
        # Create timeline structure
        timeline = {
            "timestamp": datetime.now().isoformat(),
            "project_scope": project_scope,
            "deliverables": deliverables,
            "deadline": deadline,
            "team_availability": team_availability,
            "project_timeline": {
                "project_start": "",
                "project_end": deadline,
                "phases": [],
                "milestones": [],
                "dependencies": [],
                "critical_path": [],
                "buffer_time": {}
            },
            "resource_schedule": {},
            "risk_factors": [],
            "contingency_plans": []
        }
        
        # Save timeline
        timeline_file = self.data_dir / f"project_timeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(timeline_file, 'w') as f:
            json.dump(timeline, f, indent=2)
        
        result = f"""📅 **Project Timeline Created**

**Project:** {project_scope.get('name', 'Unnamed Project')}
**Deadline:** {deadline}
**Deliverables:** {len(deliverables)} items

**Timeline Structure:**
- Project start: {timeline['project_timeline']['project_start']}
- Project end: {timeline['project_timeline']['project_end']}
- Phases: {len(timeline['project_timeline']['phases'])} phases
- Milestones: {len(timeline['project_timeline']['milestones'])} milestones
- Dependencies: {len(timeline['project_timeline']['dependencies'])} dependencies
- Critical path: {len(timeline['project_timeline']['critical_path'])} tasks

**Resource Schedule:**
{len(timeline['resource_schedule'])} resource allocations

**Risk Factors:**
{len(timeline['risk_factors'])} risks identified

**Contingency Plans:**
{len(timeline['contingency_plans'])} contingency strategies

**Next Steps:**
1. Allocate resources based on timeline
2. Set up tracking systems for milestones
3. Coordinate with team leads on schedules
4. Begin production tracking

Timeline saved to: {timeline_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("allocate_resources", "Allocate resources and manage team assignments", {
        "timeline": "dict",
        "available_resources": "dict",
        "skill_requirements": "list"
    })
    async def allocate_resources(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Allocate resources and manage team assignments."""
        timeline = args.get("timeline", {})
        available_resources = args.get("available_resources", {})
        skill_requirements = args.get("skill_requirements", [])
        
        # Create resource allocation structure
        allocation = {
            "timestamp": datetime.now().isoformat(),
            "timeline": timeline,
            "available_resources": available_resources,
            "skill_requirements": skill_requirements,
            "resource_allocation": {
                "team_assignments": {},
                "skill_mapping": {},
                "capacity_planning": {},
                "workload_distribution": {},
                "resource_conflicts": [],
                "optimization_opportunities": []
            },
            "resource_schedule": {},
            "capacity_analysis": {},
            "recommendations": []
        }
        
        # Save allocation
        allocation_file = self.data_dir / f"resource_allocation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(allocation_file, 'w') as f:
            json.dump(allocation, f, indent=2)
        
        result = f"""👥 **Resources Allocated**

**Available Resources:** {len(available_resources)} team members
**Skill Requirements:** {len(skill_requirements)} requirements

**Resource Allocation:**
- Team assignments: {len(allocation['resource_allocation']['team_assignments'])} assignments
- Skill mapping: {len(allocation['resource_allocation']['skill_mapping'])} mappings
- Capacity planning: {len(allocation['resource_allocation']['capacity_planning'])} plans
- Workload distribution: {len(allocation['resource_allocation']['workload_distribution'])} distributions
- Resource conflicts: {len(allocation['resource_allocation']['resource_conflicts'])} conflicts
- Optimization opportunities: {len(allocation['resource_allocation']['optimization_opportunities'])} opportunities

**Resource Schedule:**
{len(allocation['resource_schedule'])} scheduled allocations

**Capacity Analysis:**
{len(allocation['capacity_analysis'])} capacity assessments

**Recommendations:**
{len(allocation['recommendations'])} optimization recommendations

**Next Steps:**
1. Communicate assignments to team members
2. Set up resource tracking systems
3. Monitor capacity utilization
4. Optimize based on performance

Allocation saved to: {allocation_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("track_production", "Track production progress and manage milestones", {
        "project_id": "str",
        "milestones": "list",
        "current_status": "dict"
    })
    async def track_production(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Track production progress and manage milestones."""
        project_id = args.get("project_id", "")
        milestones = args.get("milestones", [])
        current_status = args.get("current_status", {})
        
        # Create tracking structure
        tracking = {
            "timestamp": datetime.now().isoformat(),
            "project_id": project_id,
            "milestones": milestones,
            "current_status": current_status,
            "production_tracking": {
                "overall_progress": 0,
                "milestone_status": {},
                "completed_tasks": [],
                "in_progress_tasks": [],
                "upcoming_tasks": [],
                "blocked_tasks": [],
                "delays": [],
                "quality_issues": []
            },
            "performance_metrics": {},
            "risk_alerts": [],
            "recommendations": []
        }
        
        # Save tracking
        tracking_file = self.data_dir / f"production_tracking_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(tracking_file, 'w') as f:
            json.dump(tracking, f, indent=2)
        
        result = f"""📊 **Production Tracking Update**

**Project ID:** {project_id}
**Milestones:** {len(milestones)} milestones

**Production Status:**
- Overall progress: {tracking['production_tracking']['overall_progress']}%
- Milestone status: {len(tracking['production_tracking']['milestone_status'])} milestones tracked
- Completed tasks: {len(tracking['production_tracking']['completed_tasks'])} tasks
- In progress tasks: {len(tracking['production_tracking']['in_progress_tasks'])} tasks
- Upcoming tasks: {len(tracking['production_tracking']['upcoming_tasks'])} tasks
- Blocked tasks: {len(tracking['production_tracking']['blocked_tasks'])} tasks
- Delays: {len(tracking['production_tracking']['delays'])} delays
- Quality issues: {len(tracking['production_tracking']['quality_issues'])} issues

**Performance Metrics:**
{len(tracking['performance_metrics'])} metrics tracked

**Risk Alerts:**
{len(tracking['risk_alerts'])} alerts active

**Recommendations:**
{len(tracking['recommendations'])} recommendations provided

**Next Steps:**
1. Address blocked tasks and delays
2. Resolve quality issues
3. Update timeline based on progress
4. Communicate status to stakeholders

Tracking saved to: {tracking_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("manage_vendors", "Manage vendor relationships and external resources", {
        "vendor_list": "list",
        "project_requirements": "dict",
        "budget": "dict"
    })
    async def manage_vendors(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Manage vendor relationships and external resources."""
        vendor_list = args.get("vendor_list", [])
        project_requirements = args.get("project_requirements", {})
        budget = args.get("budget", {})
        
        # Create vendor management structure
        vendor_management = {
            "timestamp": datetime.now().isoformat(),
            "vendor_list": vendor_list,
            "project_requirements": project_requirements,
            "budget": budget,
            "vendor_management": {
                "vendor_selection": {},
                "contract_negotiations": {},
                "performance_tracking": {},
                "quality_standards": {},
                "delivery_schedules": {},
                "cost_management": {}
            },
            "vendor_performance": {},
            "cost_analysis": {},
            "recommendations": []
        }
        
        # Save vendor management
        vendor_file = self.data_dir / f"vendor_management_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(vendor_file, 'w') as f:
            json.dump(vendor_management, f, indent=2)
        
        result = f"""🤝 **Vendor Management**

**Vendors:** {len(vendor_list)} vendors
**Budget:** {budget.get('total', 'Not specified')}

**Vendor Management:**
- Vendor selection: {len(vendor_management['vendor_management']['vendor_selection'])} selections
- Contract negotiations: {len(vendor_management['vendor_management']['contract_negotiations'])} negotiations
- Performance tracking: {len(vendor_management['vendor_management']['performance_tracking'])} trackings
- Quality standards: {len(vendor_management['vendor_management']['quality_standards'])} standards
- Delivery schedules: {len(vendor_management['vendor_management']['delivery_schedules'])} schedules
- Cost management: {len(vendor_management['vendor_management']['cost_management'])} cost controls

**Vendor Performance:**
{len(vendor_management['vendor_performance'])} performance assessments

**Cost Analysis:**
{len(vendor_management['cost_analysis'])} cost evaluations

**Recommendations:**
{len(vendor_management['recommendations'])} vendor recommendations

**Next Steps:**
1. Finalize vendor contracts
2. Set up performance tracking
3. Monitor delivery schedules
4. Optimize vendor relationships

Vendor management saved to: {vendor_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}
    
    @tool("coordinate_deliverables", "Coordinate deliverables and ensure quality control", {
        "deliverables": "list",
        "quality_standards": "dict",
        "review_process": "dict"
    })
    async def coordinate_deliverables(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate deliverables and ensure quality control."""
        deliverables = args.get("deliverables", [])
        quality_standards = args.get("quality_standards", {})
        review_process = args.get("review_process", {})
        
        # Create deliverable coordination structure
        coordination = {
            "timestamp": datetime.now().isoformat(),
            "deliverables": deliverables,
            "quality_standards": quality_standards,
            "review_process": review_process,
            "deliverable_coordination": {
                "delivery_schedule": {},
                "quality_checkpoints": [],
                "review_assignments": {},
                "approval_workflow": {},
                "revision_process": {},
                "final_delivery": {}
            },
            "quality_control": {
                "standards_compliance": {},
                "quality_issues": [],
                "improvement_actions": [],
                "quality_metrics": {}
            },
            "delivery_status": {},
            "recommendations": []
        }
        
        # Save coordination
        coordination_file = self.data_dir / f"deliverable_coordination_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(coordination_file, 'w') as f:
            json.dump(coordination, f, indent=2)
        
        result = f"""📦 **Deliverable Coordination**

**Deliverables:** {len(deliverables)} items
**Quality Standards:** {len(quality_standards)} standards

**Deliverable Coordination:**
- Delivery schedule: {len(coordination['deliverable_coordination']['delivery_schedule'])} scheduled items
- Quality checkpoints: {len(coordination['deliverable_coordination']['quality_checkpoints'])} checkpoints
- Review assignments: {len(coordination['deliverable_coordination']['review_assignments'])} assignments
- Approval workflow: {len(coordination['deliverable_coordination']['approval_workflow'])} workflow steps
- Revision process: {len(coordination['deliverable_coordination']['revision_process'])} revision steps
- Final delivery: {len(coordination['deliverable_coordination']['final_delivery'])} delivery items

**Quality Control:**
- Standards compliance: {len(coordination['quality_control']['standards_compliance'])} compliance checks
- Quality issues: {len(coordination['quality_control']['quality_issues'])} issues identified
- Improvement actions: {len(coordination['quality_control']['improvement_actions'])} actions
- Quality metrics: {len(coordination['quality_control']['quality_metrics'])} metrics

**Delivery Status:**
{len(coordination['delivery_status'])} status updates

**Recommendations:**
{len(coordination['recommendations'])} coordination recommendations

**Next Steps:**
1. Execute delivery schedule
2. Conduct quality checkpoints
3. Manage review and approval process
4. Ensure final delivery standards

Coordination saved to: {coordination_file.name}"""
        
        return {"content": [{"type": "text", "text": result}]}


async def main():
    """Main entry point for the Production Manager agent."""
    config_dir = Path("sub-agents/production-manager")
    agent = ProductionManagerAgent(config_dir)
    
    print("⚙️ Production Manager Agent")
    print("=" * 50)
    print("Welcome! I'm your AI Production Manager specializing in:")
    print("• Project timeline management and scheduling")
    print("• Resource allocation and capacity planning")
    print("• Production tracking and milestone management")
    print("• Vendor management and procurement")
    print("• Quality control and deliverable coordination")
    print()
    print("I work with all creative teams to ensure your projects")
    print("are delivered on time, on budget, and to the highest quality.")
    print()
    
    async with agent:
        await agent.run_interactive()


if __name__ == "__main__":
    asyncio.run(main())

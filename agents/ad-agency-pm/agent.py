#!/usr/bin/env python3
"""
Ad Agency Project Manager Agent

An AI-powered project management assistant for advertising agencies.
Helps manage clients, projects, tasks, deadlines, and team coordination.
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

from shared.agents import InteractiveAgent
from claude_agent_sdk import tool


class AdAgencyProjectManager(InteractiveAgent):
    """
    Project Manager Agent for Advertising Agencies.
    
    Manages clients, projects, tasks, deadlines, and team coordination
    for creative advertising agencies.
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        super().__init__(config_dir)
        self.data_dir = self.config_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize data files
        self.clients_file = self.data_dir / "clients.json"
        self.projects_file = self.data_dir / "projects.json"
        self.tasks_file = self.data_dir / "tasks.json"
        self.team_file = self.data_dir / "team.json"
        
        # Load existing data
        self.clients = self._load_data(self.clients_file, {})
        self.projects = self._load_data(self.projects_file, {})
        self.tasks = self._load_data(self.tasks_file, {})
        self.team = self._load_data(self.team_file, {})
        
        self.logger.info("Ad Agency Project Manager initialized")
    
    def _load_data(self, file_path: Path, default: Any) -> Any:
        """Load data from JSON file with fallback to default."""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.warning(f"Failed to load {file_path}: {e}")
        return default
    
    def _save_data(self, file_path: Path, data: Any) -> None:
        """Save data to JSON file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save {file_path}: {e}")
    
    def get_custom_tools(self) -> List[Any]:
        """Return list of custom tools for project management."""
        return [
            self.create_client,
            self.create_project,
            self.add_task,
            self.assign_task,
            self.update_progress,
            self.set_deadline,
            self.track_budget,
            self.generate_report,
            self.schedule_meeting,
            self.manage_team,
            self.analyze_performance,
            self.get_client_info,
            self.get_project_status,
            self.get_team_workload,
            self.get_upcoming_deadlines
        ]
    
    # Client Management Tools
    
    @tool("create_client", "Create a new client profile with contact information and preferences", {
        "name": str,
        "company": str,
        "email": str,
        "phone": str,
        "industry": str,
        "budget_range": str,
        "preferences": str
    })
    async def create_client(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new client profile."""
        client_id = str(uuid.uuid4())
        client_data = {
            "id": client_id,
            "name": args["name"],
            "company": args["company"],
            "email": args["email"],
            "phone": args["phone"],
            "industry": args["industry"],
            "budget_range": args["budget_range"],
            "preferences": args["preferences"],
            "created_at": datetime.now().isoformat(),
            "projects": [],
            "status": "active"
        }
        
        self.clients[client_id] = client_data
        self._save_data(self.clients_file, self.clients)
        
        return {
            "content": [{
                "type": "text",
                "text": f"✅ Client created successfully!\n\n"
                       f"**Client ID**: {client_id}\n"
                       f"**Name**: {client_data['name']}\n"
                       f"**Company**: {client_data['company']}\n"
                       f"**Industry**: {client_data['industry']}\n"
                       f"**Budget Range**: {client_data['budget_range']}\n"
                       f"**Created**: {client_data['created_at']}"
            }]
        }
    
    @tool("get_client_info", "Get detailed information about a client", {
        "client_id": str
    })
    async def get_client_info(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get client information."""
        client_id = args["client_id"]
        
        if client_id not in self.clients:
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Client with ID {client_id} not found."
                }]
            }
        
        client = self.clients[client_id]
        project_count = len(client.get("projects", []))
        
        return {
            "content": [{
                "type": "text",
                "text": f"📋 **Client Information**\n\n"
                       f"**Name**: {client['name']}\n"
                       f"**Company**: {client['company']}\n"
                       f"**Email**: {client['email']}\n"
                       f"**Phone**: {client['phone']}\n"
                       f"**Industry**: {client['industry']}\n"
                       f"**Budget Range**: {client['budget_range']}\n"
                       f"**Preferences**: {client['preferences']}\n"
                       f"**Projects**: {project_count}\n"
                       f"**Status**: {client['status']}\n"
                       f"**Created**: {client['created_at']}"
            }]
        }
    
    # Project Management Tools
    
    @tool("create_project", "Create a new project with timeline, budget, and team assignments", {
        "name": str,
        "client_id": str,
        "project_type": str,
        "description": str,
        "budget": float,
        "start_date": str,
        "end_date": str,
        "team_members": str
    })
    async def create_project(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new project."""
        if args["client_id"] not in self.clients:
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Client with ID {args['client_id']} not found. Please create the client first."
                }]
            }
        
        project_id = str(uuid.uuid4())
        project_data = {
            "id": project_id,
            "name": args["name"],
            "client_id": args["client_id"],
            "project_type": args["project_type"],
            "description": args["description"],
            "budget": args["budget"],
            "start_date": args["start_date"],
            "end_date": args["end_date"],
            "team_members": args["team_members"].split(",") if args["team_members"] else [],
            "status": "Not Started",
            "progress": 0,
            "phases": self.config.get("project_management", {}).get("phases", []),
            "tasks": [],
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        self.projects[project_id] = project_data
        
        # Add project to client
        self.clients[args["client_id"]]["projects"].append(project_id)
        
        self._save_data(self.projects_file, self.projects)
        self._save_data(self.clients_file, self.clients)
        
        return {
            "content": [{
                "type": "text",
                "text": f"🚀 **Project Created Successfully!**\n\n"
                       f"**Project ID**: {project_id}\n"
                       f"**Name**: {project_data['name']}\n"
                       f"**Client**: {self.clients[args['client_id']]['name']}\n"
                       f"**Type**: {project_data['project_type']}\n"
                       f"**Budget**: ${project_data['budget']:,.2f}\n"
                       f"**Timeline**: {project_data['start_date']} to {project_data['end_date']}\n"
                       f"**Team**: {', '.join(project_data['team_members']) if project_data['team_members'] else 'Not assigned'}\n"
                       f"**Status**: {project_data['status']}\n"
                       f"**Created**: {project_data['created_at']}"
            }]
        }
    
    @tool("get_project_status", "Get current status and progress of a project", {
        "project_id": str
    })
    async def get_project_status(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get project status and progress."""
        project_id = args["project_id"]
        
        if project_id not in self.projects:
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Project with ID {project_id} not found."
                }]
            }
        
        project = self.projects[project_id]
        client = self.clients.get(project["client_id"], {})
        task_count = len(project.get("tasks", []))
        
        # Calculate days remaining
        try:
            end_date = datetime.fromisoformat(project["end_date"])
            days_remaining = (end_date - datetime.now()).days
        except:
            days_remaining = "Unknown"
        
        return {
            "content": [{
                "type": "text",
                "text": f"📊 **Project Status Report**\n\n"
                       f"**Project**: {project['name']}\n"
                       f"**Client**: {client.get('name', 'Unknown')}\n"
                       f"**Type**: {project['project_type']}\n"
                       f"**Status**: {project['status']}\n"
                       f"**Progress**: {project['progress']}%\n"
                       f"**Budget**: ${project['budget']:,.2f}\n"
                       f"**Timeline**: {project['start_date']} → {project['end_date']}\n"
                       f"**Days Remaining**: {days_remaining}\n"
                       f"**Tasks**: {task_count}\n"
                       f"**Team**: {', '.join(project['team_members']) if project['team_members'] else 'Not assigned'}\n"
                       f"**Last Updated**: {project['last_updated']}"
            }]
        }
    
    # Task Management Tools
    
    @tool("add_task", "Add a new task to a project with priority and deadline", {
        "project_id": str,
        "title": str,
        "description": str,
        "priority": str,
        "deadline": str,
        "phase": str
    })
    async def add_task(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new task to a project."""
        project_id = args["project_id"]
        
        if project_id not in self.projects:
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Project with ID {project_id} not found."
                }]
            }
        
        task_id = str(uuid.uuid4())
        task_data = {
            "id": task_id,
            "project_id": project_id,
            "title": args["title"],
            "description": args["description"],
            "priority": args["priority"],
            "deadline": args["deadline"],
            "phase": args["phase"],
            "status": "Not Started",
            "assigned_to": None,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        self.tasks[task_id] = task_data
        self.projects[project_id]["tasks"].append(task_id)
        self.projects[project_id]["last_updated"] = datetime.now().isoformat()
        
        self._save_data(self.tasks_file, self.tasks)
        self._save_data(self.projects_file, self.projects)
        
        return {
            "content": [{
                "type": "text",
                "text": f"✅ **Task Added Successfully!**\n\n"
                       f"**Task ID**: {task_id}\n"
                       f"**Title**: {task_data['title']}\n"
                       f"**Project**: {self.projects[project_id]['name']}\n"
                       f"**Priority**: {task_data['priority']}\n"
                       f"**Deadline**: {task_data['deadline']}\n"
                       f"**Phase**: {task_data['phase']}\n"
                       f"**Status**: {task_data['status']}\n"
                       f"**Created**: {task_data['created_at']}"
            }]
        }
    
    @tool("assign_task", "Assign a task to a team member", {
        "task_id": str,
        "assigned_to": str
    })
    async def assign_task(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Assign a task to a team member."""
        task_id = args["task_id"]
        
        if task_id not in self.tasks:
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Task with ID {task_id} not found."
                }]
            }
        
        self.tasks[task_id]["assigned_to"] = args["assigned_to"]
        self.tasks[task_id]["last_updated"] = datetime.now().isoformat()
        
        self._save_data(self.tasks_file, self.tasks)
        
        return {
            "content": [{
                "type": "text",
                "text": f"👤 **Task Assigned Successfully!**\n\n"
                       f"**Task**: {self.tasks[task_id]['title']}\n"
                       f"**Assigned to**: {args['assigned_to']}\n"
                       f"**Project**: {self.projects[self.tasks[task_id]['project_id']]['name']}\n"
                       f"**Deadline**: {self.tasks[task_id]['deadline']}\n"
                       f"**Priority**: {self.tasks[task_id]['priority']}"
            }]
        }
    
    @tool("update_progress", "Update task or project progress", {
        "item_id": str,
        "item_type": str,
        "progress": int,
        "status": str,
        "notes": str
    })
    async def update_progress(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Update progress for a task or project."""
        item_id = args["item_id"]
        item_type = args["item_type"]
        progress = args["progress"]
        status = args["status"]
        notes = args.get("notes", "")
        
        if item_type == "task":
            if item_id not in self.tasks:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"❌ Task with ID {item_id} not found."
                    }]
                }
            
            self.tasks[item_id]["status"] = status
            self.tasks[item_id]["last_updated"] = datetime.now().isoformat()
            if notes:
                self.tasks[item_id]["notes"] = notes
            
            self._save_data(self.tasks_file, self.tasks)
            
            return {
                "content": [{
                    "type": "text",
                    "text": f"📈 **Task Progress Updated!**\n\n"
                           f"**Task**: {self.tasks[item_id]['title']}\n"
                           f"**Status**: {status}\n"
                           f"**Notes**: {notes if notes else 'No additional notes'}\n"
                           f"**Updated**: {self.tasks[item_id]['last_updated']}"
                }]
            }
        
        elif item_type == "project":
            if item_id not in self.projects:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"❌ Project with ID {item_id} not found."
                    }]
                }
            
            self.projects[item_id]["status"] = status
            self.projects[item_id]["progress"] = progress
            self.projects[item_id]["last_updated"] = datetime.now().isoformat()
            if notes:
                self.projects[item_id]["notes"] = notes
            
            self._save_data(self.projects_file, self.projects)
            
            return {
                "content": [{
                    "type": "text",
                    "text": f"📊 **Project Progress Updated!**\n\n"
                           f"**Project**: {self.projects[item_id]['name']}\n"
                           f"**Status**: {status}\n"
                           f"**Progress**: {progress}%\n"
                           f"**Notes**: {notes if notes else 'No additional notes'}\n"
                           f"**Updated**: {self.projects[item_id]['last_updated']}"
                }]
            }
        
        return {
            "content": [{
                "type": "text",
                "text": f"❌ Invalid item type. Use 'task' or 'project'."
            }]
        }
    
    # Deadline and Timeline Management
    
    @tool("set_deadline", "Set or update deadline for a task or project", {
        "item_id": str,
        "item_type": str,
        "deadline": str,
        "reason": str
    })
    async def set_deadline(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Set or update deadline for a task or project."""
        item_id = args["item_id"]
        item_type = args["item_type"]
        deadline = args["deadline"]
        reason = args.get("reason", "No reason provided")
        
        if item_type == "task":
            if item_id not in self.tasks:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"❌ Task with ID {item_id} not found."
                    }]
                }
            
            old_deadline = self.tasks[item_id]["deadline"]
            self.tasks[item_id]["deadline"] = deadline
            self.tasks[item_id]["last_updated"] = datetime.now().isoformat()
            
            self._save_data(self.tasks_file, self.tasks)
            
            return {
                "content": [{
                    "type": "text",
                    "text": f"⏰ **Task Deadline Updated!**\n\n"
                           f"**Task**: {self.tasks[item_id]['title']}\n"
                           f"**Old Deadline**: {old_deadline}\n"
                           f"**New Deadline**: {deadline}\n"
                           f"**Reason**: {reason}\n"
                           f"**Updated**: {self.tasks[item_id]['last_updated']}"
                }]
            }
        
        elif item_type == "project":
            if item_id not in self.projects:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"❌ Project with ID {item_id} not found."
                    }]
                }
            
            old_deadline = self.projects[item_id]["end_date"]
            self.projects[item_id]["end_date"] = deadline
            self.projects[item_id]["last_updated"] = datetime.now().isoformat()
            
            self._save_data(self.projects_file, self.projects)
            
            return {
                "content": [{
                    "type": "text",
                    "text": f"📅 **Project Deadline Updated!**\n\n"
                           f"**Project**: {self.projects[item_id]['name']}\n"
                           f"**Old Deadline**: {old_deadline}\n"
                           f"**New Deadline**: {deadline}\n"
                           f"**Reason**: {reason}\n"
                           f"**Updated**: {self.projects[item_id]['last_updated']}"
                }]
            }
        
        return {
            "content": [{
                "type": "text",
                "text": f"❌ Invalid item type. Use 'task' or 'project'."
            }]
        }
    
    @tool("get_upcoming_deadlines", "Get all upcoming deadlines for tasks and projects", {
        "days_ahead": int
    })
    async def get_upcoming_deadlines(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get upcoming deadlines."""
        days_ahead = args.get("days_ahead", 7)
        cutoff_date = datetime.now() + timedelta(days=days_ahead)
        
        upcoming_tasks = []
        upcoming_projects = []
        
        # Check task deadlines
        for task_id, task in self.tasks.items():
            try:
                deadline = datetime.fromisoformat(task["deadline"])
                if datetime.now() <= deadline <= cutoff_date:
                    upcoming_tasks.append({
                        "id": task_id,
                        "title": task["title"],
                        "deadline": task["deadline"],
                        "priority": task["priority"],
                        "assigned_to": task.get("assigned_to", "Unassigned"),
                        "project": self.projects[task["project_id"]]["name"]
                    })
            except:
                continue
        
        # Check project deadlines
        for project_id, project in self.projects.items():
            try:
                deadline = datetime.fromisoformat(project["end_date"])
                if datetime.now() <= deadline <= cutoff_date:
                    upcoming_projects.append({
                        "id": project_id,
                        "name": project["name"],
                        "deadline": project["end_date"],
                        "status": project["status"],
                        "progress": project["progress"]
                    })
            except:
                continue
        
        # Sort by deadline
        upcoming_tasks.sort(key=lambda x: x["deadline"])
        upcoming_projects.sort(key=lambda x: x["deadline"])
        
        result_text = f"📅 **Upcoming Deadlines (Next {days_ahead} Days)**\n\n"
        
        if upcoming_tasks:
            result_text += "**🔸 TASKS:**\n"
            for task in upcoming_tasks:
                result_text += f"• {task['title']} - {task['deadline']} ({task['priority']} priority)\n"
                result_text += f"  Project: {task['project']} | Assigned to: {task['assigned_to']}\n\n"
        
        if upcoming_projects:
            result_text += "**🔸 PROJECTS:**\n"
            for project in upcoming_projects:
                result_text += f"• {project['name']} - {project['deadline']}\n"
                result_text += f"  Status: {project['status']} | Progress: {project['progress']}%\n\n"
        
        if not upcoming_tasks and not upcoming_projects:
            result_text += "✅ No upcoming deadlines in the next {days_ahead} days!"
        
        return {
            "content": [{
                "type": "text",
                "text": result_text
            }]
        }
    
    # Budget Management
    
    @tool("track_budget", "Track and update project budget allocation", {
        "project_id": str,
        "category": str,
        "amount": float,
        "description": str
    })
    async def track_budget(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Track budget allocation for a project."""
        project_id = args["project_id"]
        
        if project_id not in self.projects:
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Project with ID {project_id} not found."
                }]
            }
        
        # Initialize budget tracking if not exists
        if "budget_tracking" not in self.projects[project_id]:
            self.projects[project_id]["budget_tracking"] = {}
        
        category = args["category"]
        amount = args["amount"]
        description = args["description"]
        
        if category not in self.projects[project_id]["budget_tracking"]:
            self.projects[project_id]["budget_tracking"][category] = []
        
        expense = {
            "id": str(uuid.uuid4()),
            "amount": amount,
            "description": description,
            "date": datetime.now().isoformat()
        }
        
        self.projects[project_id]["budget_tracking"][category].append(expense)
        self.projects[project_id]["last_updated"] = datetime.now().isoformat()
        
        self._save_data(self.projects_file, self.projects)
        
        # Calculate totals
        total_budget = self.projects[project_id]["budget"]
        total_spent = sum(
            sum(expense["amount"] for expense in expenses)
            for expenses in self.projects[project_id]["budget_tracking"].values()
        )
        remaining = total_budget - total_spent
        
        return {
            "content": [{
                "type": "text",
                "text": f"💰 **Budget Updated!**\n\n"
                       f"**Project**: {self.projects[project_id]['name']}\n"
                       f"**Category**: {category}\n"
                       f"**Amount**: ${amount:,.2f}\n"
                       f"**Description**: {description}\n\n"
                       f"**Budget Summary:**\n"
                       f"• Total Budget: ${total_budget:,.2f}\n"
                       f"• Total Spent: ${total_spent:,.2f}\n"
                       f"• Remaining: ${remaining:,.2f}\n"
                       f"• Utilization: {(total_spent/total_budget)*100:.1f}%"
            }]
        }
    
    # Team Management
    
    @tool("manage_team", "Manage team member information and workload", {
        "action": str,
        "name": str,
        "role": str,
        "email": str,
        "capacity": int
    })
    async def manage_team(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Manage team member information."""
        action = args["action"]
        name = args["name"]
        
        if action == "add":
            member_id = str(uuid.uuid4())
            member_data = {
                "id": member_id,
                "name": name,
                "role": args["role"],
                "email": args["email"],
                "capacity": args.get("capacity", 100),  # Percentage
                "current_workload": 0,
                "projects": [],
                "created_at": datetime.now().isoformat()
            }
            
            self.team[member_id] = member_data
            self._save_data(self.team_file, self.team)
            
            return {
                "content": [{
                    "type": "text",
                    "text": f"👥 **Team Member Added!**\n\n"
                           f"**Name**: {name}\n"
                           f"**Role**: {args['role']}\n"
                           f"**Email**: {args['email']}\n"
                           f"**Capacity**: {args.get('capacity', 100)}%\n"
                           f"**ID**: {member_id}"
                }]
            }
        
        elif action == "remove":
            # Find member by name
            member_id = None
            for mid, member in self.team.items():
                if member["name"].lower() == name.lower():
                    member_id = mid
                    break
            
            if member_id:
                del self.team[member_id]
                self._save_data(self.team_file, self.team)
                return {
                    "content": [{
                        "type": "text",
                        "text": f"👥 **Team Member Removed!**\n\n**Name**: {name}"
                    }]
                }
            else:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"❌ Team member '{name}' not found."
                    }]
                }
        
        return {
            "content": [{
                "type": "text",
                "text": f"❌ Invalid action. Use 'add' or 'remove'."
            }]
        }
    
    @tool("get_team_workload", "Get current workload and capacity of team members", {})
    async def get_team_workload(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get team workload overview."""
        if not self.team:
            return {
                "content": [{
                    "type": "text",
                    "text": "👥 **Team Workload Report**\n\nNo team members found. Add team members first."
                }]
            }
        
        result_text = "👥 **Team Workload Report**\n\n"
        
        for member_id, member in self.team.items():
            capacity = member.get("capacity", 100)
            workload = member.get("current_workload", 0)
            utilization = (workload / capacity) * 100 if capacity > 0 else 0
            
            status_emoji = "🟢" if utilization < 70 else "🟡" if utilization < 90 else "🔴"
            
            result_text += f"{status_emoji} **{member['name']}** ({member['role']})\n"
            result_text += f"   Capacity: {capacity}% | Workload: {workload}% | Utilization: {utilization:.1f}%\n"
            result_text += f"   Email: {member['email']}\n\n"
        
        return {
            "content": [{
                "type": "text",
                "text": result_text
            }]
        }
    
    # Reporting and Analytics
    
    @tool("generate_report", "Generate comprehensive project or agency report", {
        "report_type": str,
        "scope": str,
        "format": str
    })
    async def generate_report(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive reports."""
        report_type = args["report_type"]
        scope = args["scope"]
        format_type = args.get("format", "summary")
        
        if report_type == "project" and scope in self.projects:
            project = self.projects[scope]
            client = self.clients.get(project["client_id"], {})
            
            # Calculate project metrics
            total_tasks = len(project.get("tasks", []))
            completed_tasks = sum(1 for task_id in project.get("tasks", []) 
                                if self.tasks.get(task_id, {}).get("status") == "Completed")
            
            # Budget analysis
            total_budget = project["budget"]
            total_spent = 0
            if "budget_tracking" in project:
                total_spent = sum(
                    sum(expense["amount"] for expense in expenses)
                    for expenses in project["budget_tracking"].values()
                )
            
            report_text = f"📊 **Project Report: {project['name']}**\n\n"
            report_text += f"**Client**: {client.get('name', 'Unknown')}\n"
            report_text += f"**Type**: {project['project_type']}\n"
            report_text += f"**Status**: {project['status']}\n"
            report_text += f"**Progress**: {project['progress']}%\n"
            report_text += f"**Timeline**: {project['start_date']} → {project['end_date']}\n"
            report_text += f"**Budget**: ${total_budget:,.2f} (Spent: ${total_spent:,.2f})\n"
            report_text += f"**Tasks**: {completed_tasks}/{total_tasks} completed\n"
            report_text += f"**Team**: {', '.join(project['team_members']) if project['team_members'] else 'Not assigned'}\n\n"
            
            if project.get("tasks"):
                report_text += "**Task Breakdown:**\n"
                for task_id in project["tasks"]:
                    task = self.tasks.get(task_id, {})
                    if task:
                        report_text += f"• {task['title']} - {task['status']} ({task['priority']})\n"
            
            return {
                "content": [{
                    "type": "text",
                    "text": report_text
                }]
            }
        
        elif report_type == "agency":
            # Agency-wide report
            total_clients = len(self.clients)
            total_projects = len(self.projects)
            total_tasks = len(self.tasks)
            total_team = len(self.team)
            
            active_projects = sum(1 for p in self.projects.values() 
                                if p["status"] in ["In Progress", "Review"])
            
            report_text = f"🏢 **Agency Overview Report**\n\n"
            report_text += f"**Clients**: {total_clients}\n"
            report_text += f"**Projects**: {total_projects} (Active: {active_projects})\n"
            report_text += f"**Tasks**: {total_tasks}\n"
            report_text += f"**Team Members**: {total_team}\n\n"
            
            if self.projects:
                report_text += "**Recent Projects:**\n"
                recent_projects = sorted(self.projects.values(), 
                                       key=lambda x: x["last_updated"], reverse=True)[:5]
                for project in recent_projects:
                    report_text += f"• {project['name']} - {project['status']} ({project['progress']}%)\n"
            
            return {
                "content": [{
                    "type": "text",
                    "text": report_text
                }]
            }
        
        return {
            "content": [{
                "type": "text",
                "text": f"❌ Invalid report type or scope. Use 'project' with project_id or 'agency'."
            }]
        }
    
    @tool("analyze_performance", "Analyze team and project performance metrics", {
        "timeframe": str,
        "metric": str
    })
    async def analyze_performance(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance metrics."""
        timeframe = args.get("timeframe", "30")
        metric = args.get("metric", "overall")
        
        # Calculate basic metrics
        total_projects = len(self.projects)
        completed_projects = sum(1 for p in self.projects.values() 
                               if p["status"] == "Completed")
        completion_rate = (completed_projects / total_projects * 100) if total_projects > 0 else 0
        
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for t in self.tasks.values() 
                            if t["status"] == "Completed")
        task_completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Calculate average project duration (simplified)
        avg_progress = sum(p["progress"] for p in self.projects.values()) / total_projects if total_projects > 0 else 0
        
        result_text = f"📈 **Performance Analysis (Last {timeframe} days)**\n\n"
        result_text += f"**Project Metrics:**\n"
        result_text += f"• Total Projects: {total_projects}\n"
        result_text += f"• Completed: {completed_projects}\n"
        result_text += f"• Completion Rate: {completion_rate:.1f}%\n"
        result_text += f"• Average Progress: {avg_progress:.1f}%\n\n"
        
        result_text += f"**Task Metrics:**\n"
        result_text += f"• Total Tasks: {total_tasks}\n"
        result_text += f"• Completed: {completed_tasks}\n"
        result_text += f"• Completion Rate: {task_completion_rate:.1f}%\n\n"
        
        # Performance insights
        if completion_rate > 80:
            result_text += "🎉 **Excellent performance!** High project completion rate.\n"
        elif completion_rate > 60:
            result_text += "👍 **Good performance.** Room for improvement in project completion.\n"
        else:
            result_text += "⚠️ **Performance needs attention.** Low project completion rate.\n"
        
        return {
            "content": [{
                "type": "text",
                "text": result_text
            }]
        }
    
    # Meeting and Communication
    
    @tool("schedule_meeting", "Schedule a meeting with team members or clients", {
        "title": str,
        "participants": str,
        "date": str,
        "time": str,
        "duration": int,
        "agenda": str
    })
    async def schedule_meeting(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule a meeting."""
        meeting_id = str(uuid.uuid4())
        meeting_data = {
            "id": meeting_id,
            "title": args["title"],
            "participants": args["participants"].split(",") if args["participants"] else [],
            "date": args["date"],
            "time": args["time"],
            "duration": args["duration"],
            "agenda": args["agenda"],
            "created_at": datetime.now().isoformat()
        }
        
        # Save meeting (simplified - in real implementation, you'd use a meetings file)
        meetings_file = self.data_dir / "meetings.json"
        meetings = self._load_data(meetings_file, {})
        meetings[meeting_id] = meeting_data
        self._save_data(meetings_file, meetings)
        
        return {
            "content": [{
                "type": "text",
                "text": f"📅 **Meeting Scheduled!**\n\n"
                       f"**Title**: {meeting_data['title']}\n"
                       f"**Date**: {meeting_data['date']}\n"
                       f"**Time**: {meeting_data['time']}\n"
                       f"**Duration**: {meeting_data['duration']} minutes\n"
                       f"**Participants**: {', '.join(meeting_data['participants']) if meeting_data['participants'] else 'None'}\n"
                       f"**Agenda**: {meeting_data['agenda']}\n"
                       f"**Meeting ID**: {meeting_id}"
            }]
        }


async def main():
    """Main entry point for the Ad Agency Project Manager agent."""
    config_dir = Path("agents/ad-agency-pm")
    agent = AdAgencyProjectManager(config_dir)
    
    print("🎯 Ad Agency Project Manager Agent")
    print("=" * 50)
    print("Welcome! I'm your AI Project Manager for advertising agencies.")
    print("I can help you manage clients, projects, tasks, deadlines, and team coordination.")
    print("\nAvailable commands:")
    print("• Create clients and projects")
    print("• Manage tasks and assignments")
    print("• Track budgets and deadlines")
    print("• Generate reports and analytics")
    print("• Schedule meetings")
    print("• Analyze team performance")
    print("\nType 'help' for more information or start with your request!")
    print("=" * 50)
    
    try:
        await agent.run_interactive()
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Your project data has been saved.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        agent.logger.error(f"Agent error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
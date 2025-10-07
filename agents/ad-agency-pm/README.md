# Ad Agency Project Manager Agent

An AI-powered project management assistant specifically designed for advertising agencies. This agent helps manage clients, projects, tasks, deadlines, team coordination, and budget tracking for creative agencies.

**🆕 NEW: Squad Mode** - Multi-agent creative collaboration with 6 specialist AI agents!

## 🎯 Overview

The Ad Agency Project Manager Agent operates in two modes:

### 🎯 Solo Mode (Traditional Project Management)
Built to handle the unique challenges of managing creative projects in advertising agencies, including:

- **Client Management**: Track client information, preferences, and project history
- **Project Planning**: Create and manage campaigns from concept to completion
- **Task Coordination**: Break down projects into manageable tasks with deadlines
- **Team Management**: Assign tasks, track workload, and coordinate team members
- **Budget Tracking**: Monitor project expenses and budget allocation
- **Timeline Management**: Set deadlines, track progress, and identify bottlenecks
- **Reporting**: Generate comprehensive reports for clients and internal use

### 🎭 Squad Mode (Multi-Agent Creative Collaboration)
Revolutionary multi-agent system where one brief is processed by 6 specialist AI agents:

- **Account Manager**: Brief analysis, client communication, requirement extraction
- **Creative Director**: Creative strategy, concept synthesis, overall vision
- **Art Director**: Visual concepts, design direction, moodboards
- **Copywriter**: Messaging, copy creation, tone of voice
- **Strategy Planner**: Market analysis, target audience, media strategy
- **Production Manager**: Timeline, resource allocation, production coordination

**Workflow**: Send a creative brief → Squad analyzes in parallel → Creative Director synthesizes → Complete campaign strategy delivered!

## 🚀 Features

### 🎯 Solo Mode Capabilities

- ✅ **Client Management**: Create and manage client profiles with contact info and preferences
- ✅ **Project Lifecycle**: Full project management from creation to completion
- ✅ **Task Management**: Create, assign, and track tasks with priorities and deadlines
- ✅ **Team Coordination**: Manage team members, roles, and workload distribution
- ✅ **Budget Tracking**: Monitor expenses by category and project
- ✅ **Timeline Management**: Set deadlines and track progress
- ✅ **Performance Analytics**: Analyze team and project performance metrics
- ✅ **Meeting Scheduling**: Schedule and manage team and client meetings
- ✅ **Reporting**: Generate detailed reports for projects and agency overview

### 🎭 Squad Mode Capabilities

- ✅ **Multi-Agent Collaboration**: 6 specialist AI agents working together
- ✅ **Parallel Analysis**: Multiple agents analyze brief simultaneously for speed
- ✅ **Specialized Expertise**: Each agent has deep knowledge in their discipline
- ✅ **Creative Synthesis**: Creative Director combines all insights into cohesive strategy
- ✅ **Workflow Orchestration**: Sequential and parallel workflow patterns
- ✅ **Context Sharing**: All agents share project context automatically
- ✅ **Delegation Tools**: Direct delegation to specific specialists
- ✅ **Squad Reviews**: Comprehensive analysis with all agents

### Project Types Supported

- 🎨 **Brand Identity**: Logo design, brand guidelines, visual identity
- 📱 **Digital Campaigns**: Social media, online advertising, web campaigns
- 🎬 **Video Production**: Commercials, social media videos, explainer videos
- 🌐 **Website Development**: Corporate sites, landing pages, e-commerce
- 📰 **Print Advertising**: Magazine ads, billboards, brochures
- 🎪 **Event Marketing**: Trade shows, product launches, corporate events
- 📝 **Content Marketing**: Blog posts, articles, white papers

### Team Roles Supported

- 👔 **Account Manager**: Client relations and project coordination
- 🎨 **Creative Director**: Overall creative vision and direction
- 🖼️ **Art Director**: Visual design and layout
- ✍️ **Copywriter**: Content creation and messaging
- 🎨 **Graphic Designer**: Visual design and assets
- 🎬 **Video Producer**: Video production and editing
- 📱 **Social Media Manager**: Social media strategy and content
- 💻 **Developer**: Technical implementation
- 📊 **Analyst**: Performance tracking and insights

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.10+
- Claude Agent SDK v0.1.0+
- Anthropic API key

### Quick Start

1. **Set up the environment** (from repository root):
   ```bash
   ./scripts/setup.sh
   source .venv/bin/activate
   ```

2. **Configure your API key** in `.env`:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

3. **Run the agent**:
   
   **Solo Mode** (Traditional Project Management):
   ```bash
   cd agents/ad-agency-pm
   python agent.py
   ```
   
   **Squad Mode** (Multi-Agent Creative Collaboration):
   ```bash
   cd agents/ad-agency-pm
   python agent.py --squad
   ```

## 📋 Usage Examples

### 1. Setting Up a New Client

```
💬 You: Create a new client for TechStart Inc.

🤖 Agent: I'll help you create a new client profile. I need some information:

- Client name: John Smith
- Company: TechStart Inc.
- Email: john@techstart.com
- Phone: +1-555-0123
- Industry: Technology
- Budget range: $50,000-$100,000
- Preferences: Modern, clean design, focus on mobile-first approach

✅ Client created successfully!
Client ID: abc123-def456-ghi789
Name: John Smith
Company: TechStart Inc.
Industry: Technology
Budget Range: $50,000-$100,000
```

### 2. Creating a New Project

```
💬 You: Create a new brand identity project for TechStart Inc.

🤖 Agent: I'll create a brand identity project for TechStart Inc. I need:

- Project name: TechStart Brand Identity
- Client ID: abc123-def456-ghi789
- Project type: Brand Identity
- Description: Complete brand identity including logo, guidelines, and applications
- Budget: $25,000
- Start date: 2025-01-15
- End date: 2025-03-15
- Team members: Creative Director, Art Director, Copywriter

🚀 Project Created Successfully!
Project ID: proj-xyz789-abc123
Name: TechStart Brand Identity
Client: TechStart Inc.
Type: Brand Identity
Budget: $25,000.00
Timeline: 2025-01-15 to 2025-03-15
Team: Creative Director, Art Director, Copywriter
Status: Not Started
```

### 3. Adding Tasks to a Project

```
💬 You: Add tasks for the brand identity project

🤖 Agent: I'll add tasks to the project. Let me create the key tasks:

1. Discovery & Strategy Phase:
   - Task: Brand Discovery Workshop
   - Priority: High
   - Deadline: 2025-01-20
   - Phase: Discovery & Strategy

2. Creative Development:
   - Task: Logo Design Concepts
   - Priority: High
   - Deadline: 2025-02-05
   - Phase: Creative Development

3. Production:
   - Task: Brand Guidelines Document
   - Priority: Medium
   - Deadline: 2025-02-28
   - Phase: Production

✅ Tasks Added Successfully!
```

### 4. Assigning Tasks to Team Members

```
💬 You: Assign the logo design task to Sarah (Art Director)

🤖 Agent: I'll assign the logo design task to Sarah.

👤 Task Assigned Successfully!
Task: Logo Design Concepts
Assigned to: Sarah (Art Director)
Project: TechStart Brand Identity
Deadline: 2025-02-05
Priority: High
```

### 5. Tracking Budget

```
💬 You: Track a $5,000 expense for design software licenses

🤖 Agent: I'll track this budget expense.

💰 Budget Updated!
Project: TechStart Brand Identity
Category: Creative Tools
Amount: $5,000.00
Description: Design software licenses (Adobe Creative Suite, Figma Pro)

Budget Summary:
• Total Budget: $25,000.00
• Total Spent: $5,000.00
• Remaining: $20,000.00
• Utilization: 20.0%
```

### 6. Generating Reports

```
💬 You: Generate a project report for TechStart Brand Identity

🤖 Agent: I'll generate a comprehensive project report.

📊 Project Report: TechStart Brand Identity

Client: TechStart Inc.
Type: Brand Identity
Status: In Progress
Progress: 35%
Timeline: 2025-01-15 → 2025-03-15
Budget: $25,000.00 (Spent: $5,000.00)
Tasks: 2/5 completed
Team: Creative Director, Art Director, Copywriter

Task Breakdown:
• Brand Discovery Workshop - Completed (High)
• Logo Design Concepts - In Progress (High)
• Brand Guidelines Document - Not Started (Medium)
• Logo Applications - Not Started (Medium)
• Final Presentation - Not Started (High)
```

### 7. Managing Team Workload

```
💬 You: Show me the current team workload

🤖 Agent: I'll show you the current team workload status.

👥 Team Workload Report

🟢 Sarah (Art Director)
   Capacity: 100% | Workload: 60% | Utilization: 60.0%
   Email: sarah@agency.com

🟡 Mike (Creative Director)
   Capacity: 100% | Workload: 85% | Utilization: 85.0%
   Email: mike@agency.com

🟢 Lisa (Copywriter)
   Capacity: 100% | Workload: 45% | Utilization: 45.0%
   Email: lisa@agency.com
```

### 8. Upcoming Deadlines

```
💬 You: Show me upcoming deadlines for the next 2 weeks

🤖 Agent: I'll show you all upcoming deadlines.

📅 Upcoming Deadlines (Next 14 Days)

🔸 TASKS:
• Logo Design Concepts - 2025-02-05 (High priority)
  Project: TechStart Brand Identity | Assigned to: Sarah (Art Director)

• Brand Guidelines Document - 2025-02-28 (Medium priority)
  Project: TechStart Brand Identity | Assigned to: Mike (Creative Director)

🔸 PROJECTS:
• TechStart Brand Identity - 2025-03-15
  Status: In Progress | Progress: 35%
```

## 🎨 Creative Agency Workflow

### Typical Project Phases

1. **Discovery & Strategy** (Week 1-2)
   - Client briefing and requirements gathering
   - Market research and competitive analysis
   - Strategy development and creative brief

2. **Creative Development** (Week 3-6)
   - Concept development and ideation
   - Initial designs and mockups
   - Client presentation and feedback

3. **Production** (Week 7-10)
   - Final design development
   - Asset creation and optimization
   - Quality assurance and testing

4. **Review & Refinement** (Week 11-12)
   - Client review and feedback
   - Revisions and refinements
   - Final approval process

5. **Launch & Optimization** (Week 13-14)
   - Deployment and launch
   - Performance monitoring
   - Initial optimization

6. **Post-Launch Analysis** (Week 15-16)
   - Performance analysis and reporting
   - Lessons learned documentation
   - Future recommendations

## 🎭 Squad Mode Examples

### 1. Creative Brief Processing

```
💬 You: We need a campaign for a new eco-friendly sneaker brand targeting Gen Z. Budget $50k, 6-week timeline.

🤖 Agent: I'll coordinate the creative squad to develop a comprehensive campaign strategy.

🎭 **Squad Analysis in Progress...**

**Account Manager**: Brief analyzed - eco-friendly sneakers, Gen Z target, $50k budget, 6 weeks
**Creative Director**: Strategic direction - sustainability meets street culture
**Art Director**: Visual concepts - nature-inspired palettes, urban photography
**Copywriter**: Messaging - "Step Light, Live Right" tagline, sustainability focus
**Strategy Planner**: Media strategy - TikTok, Instagram, influencer partnerships
**Production Manager**: Timeline - 2 weeks concept, 2 weeks production, 2 weeks launch

🎯 **Squad Synthesis** (Creative Director):
Complete campaign strategy delivered with visual concepts, messaging, media plan, and production timeline.
```

### 2. Brand Identity Development

```
💬 You: Create a brand identity for a premium coffee roastery targeting urban professionals.

🤖 Agent: I'll delegate this to the creative squad for comprehensive brand development.

🎭 **Squad Review**:
- **Account Manager**: Target audience analysis - urban professionals, coffee enthusiasts
- **Creative Director**: Brand positioning - premium, artisanal, sophisticated
- **Art Director**: Visual identity - minimalist, warm tones, coffee bean motifs
- **Copywriter**: Brand voice - sophisticated, knowledgeable, approachable
- **Strategy Planner**: Market positioning - premium segment, direct-to-consumer
- **Production Manager**: Brand rollout - 4-week development, phased launch

🎯 **Deliverables**: Complete brand guidelines, logo concepts, tone of voice, and launch strategy.
```

### 3. Social Media Campaign

```
💬 You: Develop a social media campaign for a fitness app launch targeting millennials.

🤖 Agent: I'll run a squad review to create a comprehensive social media strategy.

🎭 **Parallel Squad Analysis**:
All 6 agents analyze the brief simultaneously and provide specialized insights:

**Account Manager**: Millennial fitness trends, app market analysis
**Creative Director**: Campaign theme - "Your Journey, Your Pace"
**Art Director**: Visual style - motivational, diverse, lifestyle photography
**Copywriter**: Content pillars - motivation, education, community
**Strategy Planner**: Platform strategy - Instagram, TikTok, YouTube, Facebook
**Production Manager**: Content calendar - 8-week campaign, daily posts

🎯 **Squad Synthesis**: Complete social media strategy with content calendar, visual guidelines, and performance metrics.
```

### 4. Direct Specialist Delegation

```
💬 You: I need the Art Director to create moodboards for a luxury hotel rebrand.

🤖 Agent: I'll delegate this directly to the Art Director.

🎨 **Art Director Response**:
Creating luxury hotel moodboards with:
- Color palette: Deep blues, gold accents, warm neutrals
- Typography: Elegant serif fonts, clean sans-serif for body
- Imagery: Architectural details, luxury amenities, sophisticated lifestyle
- Style: Modern luxury, timeless elegance, premium feel

🎯 **Deliverables**: 3 moodboard concepts with color swatches, typography samples, and image references.
```

## 📊 Data Management

### Data Storage

The agent stores all data locally in JSON files within the `data/` directory:

- `clients.json` - Client profiles and information
- `projects.json` - Project details and progress
- `tasks.json` - Task assignments and status
- `team.json` - Team member information
- `meetings.json` - Scheduled meetings and agendas

### Data Backup

All data is automatically saved after each operation. For production use, consider:

- Regular backups of the `data/` directory
- Integration with cloud storage (Azure Blob Storage, AWS S3)
- Database migration for larger datasets

## 🔧 Customization

### Adding New Project Types

Edit `config.yaml` to add new project types:

```yaml
project_management:
  project_types:
    - "Brand Identity"
    - "Digital Campaign"
    - "Video Production"
    - "Website Development"
    - "Print Advertising"
    - "Event Marketing"
    - "Content Marketing"
    - "Your Custom Type"  # Add here
```

### Adding New Team Roles

```yaml
project_management:
  team_roles:
    - "Account Manager"
    - "Creative Director"
    - "Art Director"
    - "Copywriter"
    - "Graphic Designer"
    - "Video Producer"
    - "Social Media Manager"
    - "Developer"
    - "Analyst"
    - "Your Custom Role"  # Add here
```

### Customizing Budget Categories

```yaml
budget:
  default_allocations:
    creative: 40      # Creative development
    production: 30    # Production costs
    media: 20         # Media buying
    management: 10    # Project management
    your_category: 0  # Add custom categories
```

## 🚀 Advanced Features

### Performance Analytics

The agent provides insights into:

- Project completion rates
- Task completion efficiency
- Team utilization rates
- Budget utilization trends
- Timeline adherence

### Integration Possibilities

Future integrations could include:

- **Calendar Systems**: Google Calendar, Outlook integration
- **Communication Tools**: Slack, Microsoft Teams
- **Design Tools**: Figma, Adobe Creative Suite
- **Time Tracking**: Toggl, Harvest
- **CRM Systems**: Salesforce, HubSpot
- **Accounting**: QuickBooks, Xero

## 🎯 Best Practices

### Project Management

1. **Start with Discovery**: Always begin with thorough client discovery
2. **Set Clear Deadlines**: Use realistic timelines with buffer time
3. **Regular Check-ins**: Schedule regular progress reviews
4. **Document Everything**: Keep detailed records of decisions and changes
5. **Manage Scope**: Clearly define project boundaries and change processes

### Team Coordination

1. **Match Skills to Tasks**: Assign tasks based on team member expertise
2. **Monitor Workload**: Ensure balanced distribution of work
3. **Foster Communication**: Encourage regular team communication
4. **Provide Feedback**: Give constructive feedback on performance
5. **Celebrate Success**: Recognize team achievements

### Client Relations

1. **Set Expectations**: Clearly communicate timelines and deliverables
2. **Regular Updates**: Provide consistent progress updates
3. **Manage Feedback**: Handle client feedback professionally
4. **Document Changes**: Track all scope and requirement changes
5. **Deliver Quality**: Ensure high-quality deliverables

## 🐛 Troubleshooting

### Common Issues

**Agent won't start:**
- Check that ANTHROPIC_API_KEY is set in `.env`
- Verify Python 3.10+ is installed
- Ensure all dependencies are installed

**Data not saving:**
- Check write permissions in the `data/` directory
- Verify disk space is available
- Check for file locking issues

**Tools not working:**
- Verify the agent is using the correct model
- Check that all required parameters are provided
- Review the logs for error messages

### Getting Help

1. Check the logs in the `logs/` directory
2. Review the configuration in `config.yaml`
3. Test with simple commands first
4. Verify data files are not corrupted

## 📈 Roadmap

### Planned Features

- [ ] **Calendar Integration**: Sync with Google Calendar, Outlook
- [ ] **Time Tracking**: Built-in time tracking for tasks
- [ ] **Client Portal**: Web interface for client access
- [ ] **Mobile App**: Mobile interface for team members
- [ ] **Advanced Analytics**: More detailed performance metrics
- [ ] **Template Library**: Pre-built project templates
- [ ] **Automated Reporting**: Scheduled report generation
- [ ] **Integration APIs**: REST API for third-party integrations

### Community Contributions

We welcome contributions for:

- New project types and workflows
- Additional team roles and responsibilities
- Integration with popular agency tools
- Performance improvements and optimizations
- Documentation and examples

## 📄 License

[Add your license information here]

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Submit a pull request

---

**Part of the [Claude Agents Repository](../../README.md)**

**Need help?** Check the [main documentation](../../docs/) or open an issue for support.
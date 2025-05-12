# TTS Audiobook Application UI Design Specification

## Overview

The TTS Audiobook Application will feature a clean, modern interface following a three-panel layout similar to the provided mockup. The design emphasizes visual workflow representation, clear navigation, and intuitive configuration of voice settings. This document outlines the UI design specifications, components, and interaction patterns.

## Layout Structure

### Three-Panel Design

```
+---------------------+-----------------------------+------------------------+
|                     |                             |                        |
|                     |                             |                        |
|                     |                             |                        |
|  Navigation         |  Workspace /                |  Settings /            |
|  Sidebar            |  Visualization Panel        |  Configuration Panel   |
|                     |                             |                        |
|                     |                             |                        |
|                     |                             |                        |
+---------------------+-----------------------------+------------------------+
```

1. **Left Panel: Navigation Sidebar**
    
    - Width: 250px (collapsible)
    - Contains: Project navigation, tool selection, and action blocks
    - Fixed position while scrolling
2. **Center Panel: Workspace**
    
    - Flexible width (expands to fill available space)
    - Contains: Book content view, workflow visualization, processing status
    - Scrollable content
3. **Right Panel: Settings/Configuration**
    
    - Width: 320px (collapsible)
    - Contains: Voice settings, character assignments, processing options
    - Context-sensitive based on current selection

## Color Palette

```
Primary: #19BE82 (Green for actions, success states, and primary buttons)
Secondary: #6C63FF (Purple for accents and secondary actions)
Accent 1: #FF9F5A (Orange for processing nodes and warnings)
Accent 2: #FF5A5A (Red for errors and critical states)
Accent 3: #5ABAFF (Blue for information and selection)

Background: #F5F7FA (Light gray for app background)
Panel Background: #FFFFFF (White for panels)
Text Primary: #1E293B (Dark gray for primary text)
Text Secondary: #64748B (Medium gray for secondary text)
Border Color: #E2E8F0 (Light gray for borders)
```

## Typography

```
Primary Font: 'Inter', sans-serif
Heading Sizes:
  - H1: 24px, 700 weight
  - H2: 20px, 600 weight
  - H3: 16px, 600 weight
Body Text: 14px, 400 weight
Small Text: 12px, 400 weight
Line Height: 1.5
```

## Left Panel: Navigation Sidebar

### Components

1. **Project Selector**
    
    - Dropdown selector for current project
    - Project icon
    - Project name display
    - Dropdown icon for selecting other projects
2. **Search Bar**
    
    - Full-width search input
    - Placeholder: "Search projects..."
    - Icon: Magnifying glass
3. **Section Headers**
    
    - Collapsible sections with arrow indicators
    - Section name and item count badge
    - Toggle to expand/collapse section
4. **Tool Grid**
    
    - 2×2 grid of tool buttons
    - Each tool contains icon and label
    - Hover state with subtle background highlight
    - Tools include:
        - Book Import
        - Text Editor
        - Voice Assignment
        - Audio Export
5. **Library Section**
    
    - List of imported books
    - Book title and format indicator
    - Selection state for current book
    - Status indicator (processed/unprocessed)
6. **Recent Projects**
    
    - List of recently accessed projects
    - Project name and last modified date
    - Quick access to recent work

## Center Panel: Workspace

### Book Processing Workflow Visualization

1. **Workflow Canvas**
    
    - Zoomable, pannable canvas
    - Visual representation of processing pipeline
    - Connected nodes showing processing stages
    - Status indicators for each stage
2. **Processing Nodes**
    
    - Distinct node shapes for different types:
        - Circle: Start/end points
        - Rectangle: Processing stages
        - Diamond: Decision points
        - Hexagon: AI processing (Gemini API)
    - Color coding by type and status:
        - Green: Completed/Active
        - Orange: In progress/Waiting
        - Red: Error/Issue
        - Purple: AI-enhanced steps
    - Connection lines showing workflow direction
    - Progress indicators for long-running processes
3. **Stage Components**
    
    - Text Import Node
        
        - File format indicator
        - Import status
        - Page/word count
    - Text Processing Node
        
        - Segmentation status
        - Dialogue detection progress
        - Character identification status
    - Voice Assignment Node
        
        - Characters identified count
        - Voices assigned count
        - Assignment conflicts indicator
    - Audio Generation Node
        
        - Generation progress
        - Time remaining estimate
        - Audio length indicator
4. **Interactive Elements**
    
    - Click to view stage details in right panel
    - Double-click to focus on specific stage
    - Hover states with additional information
    - Error indicators with action buttons
5. **Bottom Toolbar**
    
    - Zoom controls
    - Fit to view button
    - Search within workflow
    - Quick add button
    - Reset view button

### Book Content View

1. **Text Display Area**
    
    - Paginated view of book content
    - Syntax highlighting for:
        - Dialogue (highlighted in blue)
        - Character names (highlighted in purple)
        - Narration (default text color)
2. **Navigation Controls**
    
    - Chapter selector dropdown
    - Page navigation controls
    - Bookmark functionality
3. **Text Analysis Overlay**
    
    - Character identification markers
    - Confidence indicators for AI analysis
    - User correction interface
    - Toggle to show/hide analysis

## Right Panel: Settings and Configuration

### General Configuration

1. **Panel Header**
    
    - Section title
    - Tab navigation for different settings groups:
        - General
        - Characters
        - Voices
        - Export
        - AI Settings (Gemini)
2. **Status Section**
    
    - Enable/disable toggle switches
    - Processing status indicators
    - Save/publish buttons
3. **Configuration Fields**
    
    - Input fields with labels
    - Dropdown selectors
    - Radio button groups
    - Checkbox options
    - Helper text for complex options

### Character Voice Assignment

1. **Character List**
    
    - Scrollable list of identified characters
    - Character name and dialogue count
    - Selected state for current character
    - AI badge for Gemini-identified characters
    - Filter controls for character list
2. **Voice Selection**
    
    - Voice dropdown for selected character
    - Preview audio button
    - Voice parameter sliders:
        - Pitch adjustment
        - Speaking rate
        - Emphasis level
    - Reset to default button
3. **Character Details**
    
    - Character description (AI-generated)
    - Speech pattern analysis
    - Related characters
    - Dialogue samples
    - Edit character information button

### AI Settings (Gemini Integration)

1. **API Configuration**
    
    - API key input field (masked)
    - Connection status indicator
    - Test connection button
    - Usage statistics
2. **Analysis Settings**
    
    - Analysis depth slider
        - Basic: Rule-based only
        - Standard: Basic AI analysis
        - Deep: Comprehensive AI analysis
    - Context window size control
    - Confidence threshold setting
    - Cache management options
3. **Feedback Controls**
    
    - Learn from corrections toggle
    - Reset learning button
    - Export analysis data
    - Privacy settings for API usage

## Component States

### Button States

1. **Primary Button**
    
    - Default: Green background (#19BE82), white text, rounded corners
    - Hover: Slightly darker green, subtle shadow
    - Active: Darker green with inset shadow
    - Disabled: Gray background, reduced opacity
2. **Secondary Button**
    
    - Default: White background, green border, green text
    - Hover: Light green background
    - Active: Slightly darker with inset shadow
    - Disabled: Gray border and text, reduced opacity
3. **Icon Button**
    
    - Default: Gray icon
    - Hover: Darker gray with light background
    - Active: Primary color
    - Selected: Primary color with light background

### Input States

1. **Text Input**
    
    - Default: White background, light gray border
    - Focus: White background, primary color border, subtle shadow
    - Error: White background, red border, error message below
    - Disabled: Light gray background, gray border
2. **Toggle Switch**
    
    - Off: Gray track, white thumb/handle
    - On: Green track (#19BE82), white thumb/handle
    - Disabled Off: Light gray track, gray thumb/handle
    - Disabled On: Faded green track, gray thumb/handle

### Processing Status Indicators

1. **Not Started**
    
    - Gray outline icon
    - "Not Started" label
    - No progress indicator
2. **In Progress**
    
    - Animated pulse effect
    - Orange icon (#FF9F5A)
    - Progress percentage
    - Cancel option
3. **Completed**
    
    - Green checkmark icon (#19BE82)
    - "Completed" label
    - Completion time
4. **Error**
    
    - Red error icon (#FF5A5A)
    - Error message
    - Retry button

## Interactive Elements

### Workflow Interactions

1. **Node Selection**
    
    - Click to select a processing node
    - Selected state: Highlighted border, expanded details
    - Shows related settings in right panel
2. **Connection Hovering**
    
    - Hover over connections to highlight full path
    - Shows data flowing between nodes
    - Indicates dependencies
3. **Drag and Drop**
    
    - Drag books from library to import
    - Drag characters to assign voices
    - Reorder processing steps when applicable
4. **Contextual Menus**
    
    - Right-click on nodes for actions
    - Options based on node type and state
    - Quick access to common operations

### Character Voice Assignment

1. **Voice Preview**
    
    - Hover on voice to show play button
    - Click to hear sample with current settings
    - Shows waveform visualization during playback
2. **Parameter Adjustment**
    
    - Real-time preview as parameters change
    - Visual feedback on parameter sliders
    - Reset individual parameters
    - A/B comparison testing
3. **Batch Operations**
    
    - Select multiple characters
    - Apply voice or parameters to selection
    - Group related characters

## Specific UI Screens

### 1. Project Dashboard

![Project Dashboard Wireframe]

The dashboard provides an overview of all audiobook projects with:

- Project cards showing book cover, title, author
- Progress indicator showing completion percentage
- Last modified date and processing status
- Quick action buttons (open, export, settings)
- Create new project button (prominent)
- Filter and sort controls for project list

### 2. Book Import and Setup

![Book Import Wireframe]

The import screen allows users to:

- Drag and drop book files or browse for files
- Preview book content before import
- Extract and edit metadata (title, author, etc.)
- Configure initial processing options
- Select processing template (fiction, non-fiction, etc.)
- Start import process with progress indication

### 3. Text Processing and Analysis

![Text Analysis Wireframe]

The text analysis screen shows:

- Split view with original text and processed segments
- Color-coded dialogue and narration identification
- Character tagging interface
- Confidence indicators for AI-identified elements
- Manual correction tools
- Processing progress and step navigation
- Analysis settings in right panel

### 4. Character and Voice Management

![Voice Management Wireframe]

The character management screen includes:

- Character list with importance ranking
- Voice assignment interface with preview
- Character relationship map (AI-generated)
- Voice customization controls
- Batch assignment tools
- Voice testing interface with sample text

### 5. Audiobook Generation and Export

![Audiobook Export Wireframe]

The export screen provides:

- Chapter organization and ordering
- Audio quality settings
- Metadata entry for the audiobook
- Export format selection
- Generation progress visualization
- Post-processing options
- Export destination selection

## Responsive Behavior

While primarily designed for desktop use, the interface should adapt to different screen sizes:

1. **Desktop (1920×1080 and larger)**
    
    - Full three-panel layout
    - Expanded workspace visualization
    - All features visible
2. **Laptop (1366×768 to 1920×1080)**
    
    - Three-panel layout with reduced padding
    - Slightly condensed components
    - Scrollable panels as needed
3. **Small Screens (below 1366px width)**
    
    - Collapsible side panels
    - Panel toggle buttons
    - Focus on one panel at a time when necessary
    - Preserved workflow visualization with zoom controls

## Accessibility Considerations

1. **Color Usage**
    
    - All information conveyed by color also has text or icon indicators
    - Sufficient contrast ratios for all text (WCAG AA compliant)
    - Alternative high-contrast theme available
2. **Keyboard Navigation**
    
    - Full keyboard accessibility for all interactions
    - Logical tab order through the interface
    - Keyboard shortcuts for common actions
    - Focus indicators for keyboard navigation
3. **Screen Readers**
    
    - Proper ARIA labels for all interactive elements
    - Meaningful alt text for icons and visualizations
    - Logical heading structure
    - Status updates announced appropriately
4. **Text Scaling**
    
    - Interface handles text scaling up to 200%
    - No loss of functionality with larger text
    - Responsive layout adjustments for accessibility needs

## Animation and Transitions

Subtle animations provide feedback and enhance usability:

1. **State Changes**
    
    - Smooth transitions between button states (300ms)
    - Easing functions for natural movement
    - Progress animations for long-running processes
2. **Panel Transitions**
    
    - Smooth slide animations for panel expansion/collapse
    - Fade transitions for content changes
    - Subtle scale animations for selection states
3. **Workflow Visualization**
    
    - Animated data flow along connection paths
    - Progress animations within nodes
    - Smooth transitions when focusing on nodes

## Implementation Notes

1. **Frontend Technologies**
    
    - Electron with React for UI components
    - CSS modules or styled-components for styling
    - SVG for workflow visualization
    - Web Audio API for audio visualization
2. **Component Library**
    
    - Custom component library for consistent styling
    - Reusable components for common patterns
    - Theme provider for consistent colors and styling
    - Responsive grid system for layouts
3. **Performance Considerations**
    
    - Virtualized lists for large character/segment lists
    - Canvas-based rendering for complex visualizations
    - Efficient state management to prevent re-renders
    - Asynchronous loading for right panel configurations

## Next Steps

1. **Prototyping**
    
    - Create interactive prototypes of key screens
    - Test workflow visualization interactions
    - Validate character voice assignment interface
2. **User Testing**
    
    - Conduct usability tests with target users
    - Collect feedback on workflow clarity
    - Validate information architecture
3. **Design Refinement**
    
    - Iterate on design based on feedback
    - Refine visual styling and animations
    - Finalize component specifications
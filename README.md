# Influencer Engagement & Sponsorship Coordination Platform (IESCP)

IESCP is a dynamic web platform that connects companies with social media influencers. It enables companies to create promotional campaigns and collaborate with influencers who align with their brand. Influencers can browse campaigns, express interest, or be invited to participate—facilitating seamless and strategic partnerships.

## Features

- **User Management**
  - Role-based authentication for Admins, Companies, and Influencers
  - Secure signup and login with password hashing

- **Campaign Management**
  - Companies can create, view, update, and delete campaigns
  - Influencers can browse and apply for relevant campaigns
  - Filter and search campaigns by category and visibility

- **Admin Dashboard**
  - View and manage all campaigns
  - Flag inappropriate content
  - Visualize platform statistics (companies, influencers, campaigns)

- **Request Handling**
  - Influencers express interest in campaigns via `InterestedCampaigns`
  - Companies can send direct invitations using `AdRequests`

## Tech Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy, Jinja2
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Database**: SQLite
- **Utilities**:
  - `datetime` for time operations
  - `kaleido` for generating statistics graphics


## Database Schema Overview

- `Admin`, `Company`, and `Influencer` tables for user management
- `Campaign` table with:
  - One-to-many relationships to `Admin` and `Company`
  - Many-to-many relationship with `Influencer` through:
    - `InterestedCampaigns`
    - `AdRequests`

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/iescp-platform.git
cd iescp-platform
```

### 2. Create a virtual environment

#### For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### For Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
flask run
```

## Visit the app at: http://127.0.0.1:5000/


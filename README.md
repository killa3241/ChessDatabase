# ♟️ Chess Database Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://mysql.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red.svg)](https://streamlit.io)
[![Analytics](https://img.shields.io/badge/Analytics-Enabled-purple.svg)](#)

> **A chess database system for organizing game data and providing basic analytics**

---

## 🎯 **Project Overview**

A simple chess database system designed to help organize and analyze chess game data. The system processes PGN files and provides basic statistical insights that may be useful for studying games and tracking player performance.

### **Potential Use Cases:**
- **📊 Basic Analytics**: View player statistics and game outcomes
- **🎓 Learning Tool**: Help chess enthusiasts explore game data
- **🏆 Game Organization**: Keep track of chess games in a structured way
- **📈 Simple Research**: Basic analysis for chess study purposes

---

## 🚀 **Features & Implementation**

### **🏗️ System Components**
- **PGN Parser**: Processes chess notation files to extract game information
- **Database Design**: MySQL schema for storing game data and metadata
- **Analytics Module**: Basic statistical analysis for game insights
- **Web Interface**: Streamlit-based dashboard for data visualization

### **⚡ Core Functionality**
- **File Processing**: Handles PGN file imports one at a time
- **Data Storage**: Organizes chess games in a structured database
- **Search & Filter**: Basic filtering by player, date, and game results
- **Statistics**: Simple win/loss ratios and game count summaries

---

## 🎮 **System Demonstration**
<img width="940" height="375" alt="image" src="https://github.com/user-attachments/assets/a8034ce1-9a86-4943-9bb7-340a848d5a8b" />
<img width="940" height="571" alt="image" src="https://github.com/user-attachments/assets/ef93b2f6-0356-48bd-9cf3-6935232be729" />

### **PGN Processing Pipeline**
<img width="940" height="439" alt="image" src="https://github.com/user-attachments/assets/b8cbe14e-130e-4e82-81f8-f714f30847c1" />

### **Database Query Interface**
*The Streamlit interface provides database queries with basic filtering and search options*
<img width="940" height="446" alt="image" src="https://github.com/user-attachments/assets/cb2524ee-4e01-4d1a-8afe-d61de74ea7c6" />
<img width="940" height="347" alt="image" src="https://github.com/user-attachments/assets/607384ad-e8a7-4056-9d45-51bb81345d45" />
<img width="940" height="408" alt="image" src="https://github.com/user-attachments/assets/938ac1a7-3d3c-4574-aa3c-98ec10feb583" />

### **Analytics Dashboard**
*Basic visualization of player statistics and game data*
<img width="940" height="335" alt="image" src="https://github.com/user-attachments/assets/5655706f-62d7-4bb0-89b7-6a2235b980c6" />
<img width="940" height="321" alt="image" src="https://github.com/user-attachments/assets/a4b2eb9b-77f3-442b-9daa-7dc1f0cf27ef" />
<img width="940" height="215" alt="image" src="https://github.com/user-attachments/assets/7957ec8d-56fc-4782-9412-59eda10f6e7c" />

---

## 🛠️ **Technology Stack**

<div align="center">

| **Component** | **Technology** | **Purpose** |
|---------------|----------------|-------------|
| **Database** | ![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange) | Store chess game data |
| **Backend** | ![Python](https://img.shields.io/badge/Python-3.8+-blue) | Data processing and analysis |
| **Frontend** | ![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red) | Web-based user interface |

</div>

---

## 🔍 **Available Features**

### **📊 Basic Analytics**
- **Opening Tracking**: See which openings appear most frequently in your database
- **Player Statistics**: View win/loss records and game counts for different players
- **Time Period Analysis**: Filter games by date ranges
- **Simple Insights**: Basic statistics like average game length and outcome distributions

### **🎯 Data Management**
- **Single File Import**: Process one PGN file at a time
- **Player Search**: Look up games by specific players
- **Date Filtering**: Find games within certain time periods
- **Result Analysis**: Group games by outcomes (win/loss/draw)

### **📋 Database Operations**
- **PGN Processing**: Import chess games from standard PGN format
- **Data Validation**: Basic checks for game data integrity  
- **Simple Queries**: Search and filter functionality
- **Export Options**: Basic data export capabilities

---

## ⚡ **Getting Started**

### **🚀 Setup**

```bash
# Clone the repository
git clone https://github.com/your-username/chess-database-management.git
cd chess-database-management
```

### **📊 Database Setup**

```bash
# Set up MySQL database
mysql -u root -p -e "CREATE DATABASE chess_db;"
mysql -u root -p chess_db < backend/sql/schema.sql

# Configure database connection
cp config/database.example.py config/database.py
# Edit database.py with your credentials
```

### **🎲 Import Sample Data**

```bash
# Process a single PGN file
python backend/pgn_parser.py data/sample_games.pgn
```

### **🖥️ Run the Application**

```bash
# Start the Streamlit web interface
streamlit run frontend/app.py
```

---

## 📁 **Project Structure**

```
chess-database-management/
├── 🗄️ backend/
│   ├── __pycache__/                # Python cache files
│   └── sql/
│       ├── schema.sql              # Database schema
│       └── pgn_parser.py           # PGN file processing
├── 🖥️ frontend/
│   ├── __pycache__/                # Python cache files
│   └── streamlit/
│       ├── secrets.toml            # Streamlit configuration
│       ├── assets/
│       │   └── icons/
│       │       ├── game.png        # Game page icon
│       │       ├── profiles.png    # Player profiles icon
│       │       ├── ranking.png     # Rankings icon
│       │       ├── settings.png    # Settings icon
│       │       ├── statistics.png  # Statistics icon
│       │       ├── support.png     # Support icon
│       │       ├── tournament.png  # Tournament icon
│       │       └── user.png        # User profile icon
│       ├── admin.py                # Admin interface
│       ├── app.py                  # Main Streamlit application
│       ├── db_utils.py             # Database utility functions
│       ├── games.py                # Game management page
│       ├── home.py                 # Home page
│       ├── login.py                # Login functionality
│       ├── navbar.py               # Navigation bar component
│       ├── rankings.py             # Player rankings page
│       ├── statistics.py           # Statistics dashboard
│       ├── support.py              # Support page
│       ├── tournaments.py          # Tournament management
│       └── yourprofile.py          # User profile page
├── .gitignore                      # Git ignore file
└── README.md                       # Project documentation
```

---

## 💡 **Future Ideas**

### **🔮 Possible Improvements**
- [ ] **Better Visualization**: More interactive charts and graphs
- [ ] **Export Features**: Additional data export formats
- [ ] **Mobile View**: Better mobile browser compatibility
- [ ] **Batch Processing**: Handle multiple PGN files at once

### **🚀 Potential Enhancements**
- [ ] **Pattern Detection**: Simple tactical pattern recognition
- [ ] **Tournament View**: Group games by tournaments
- [ ] **Player Profiles**: More detailed player information pages
- [ ] **API Development**: Simple REST API for data access

---

## 📋 **About This Project**

### **💼 Purpose**
- **Learning Project**: Built to explore database design and web development
- **Chess Enthusiast Tool**: Simple utility for organizing chess game data
- **Open Source**: Available for others to learn from and improve upon
- **Educational**: Demonstrates basic concepts in data management and visualization

### **🔧 Technical Notes**
- **Simple Design**: Focuses on core functionality over advanced features
- **Standard Tools**: Uses well-established technologies and libraries
- **Beginner Friendly**: Code structure aims to be readable and educational
- **Cross-Platform**: Works on different operating systems with Python support

<div align="center">

**⭐ If you find this project helpful, feel free to star it!**

*A simple tool for chess game organization and basic analysis*

[![GitHub stars](https://img.shields.io/github/stars/your-username/chess-database-management?style=social)](https://github.com/your-username/chess-database-management)

</div>

---

## 📄 **License & Attribution**

This project is licensed under the MIT License. If you use this system in your research or applications:

```bibtex
@software{chess_database_management,
  author = {Anikait},
  title = {Chess Database Management System},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/your-username/chess-database-management}
}
```

**Built with ♟️ for organizing and exploring chess game data**

# 🎲 D&D Combat Game

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-82%20passed-success.svg)](tests/)
[![Coverage](https://img.shields.io/badge/coverage-77%25-yellow.svg)](tests/)
[![Type Checked](https://img.shields.io/badge/mypy-strict-success.svg)](https://mypy.readthedocs.io/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A fully-featured, text-based Dungeons & Dragons combat simulator with **AI-powered narration** using OpenAI's GPT-4. Built with professional software engineering practices including comprehensive testing, strict type checking, and clean architecture.

![Combat Example](https://img.shields.io/badge/Combat-Epic%20AI%20Narration-purple.svg)

## ✨ Features

### 🎮 Core Gameplay
- **4 Playable Races**: Human, Elf, Dwarf, and Halfling - each with unique stat bonuses
- **10 Weapon Types**: From daggers to greatswords, each with distinct damage profiles
- **Turn-Based Combat**: Initiative system with strategic decision-making
- **Character Progression**: Experience points and leveling system with HP increases

### 🔮 Magic System
- **Functional Spellcasting**: Damage and healing spells with mana management
- **Spell Slots**: Traditional D&D-style resource management
- **7 Spells**: From cantrips (Fire Bolt) to healing magic (Cure Wounds)
- **Rest Mechanic**: Restore HP and spell slots between battles

### 🤖 AI Dungeon Master
- **Dynamic Narration**: OpenAI GPT-4 powered combat descriptions
- **Contextual Storytelling**: Unique narration for attacks, misses, spells, and deaths
- **Immersive Experience**: Every battle feels unique and cinematic

### 💻 Technical Excellence
- **82 Unit Tests**: Comprehensive test coverage with pytest
- **77% Code Coverage**: Well-tested codebase
- **Strict Type Checking**: 100% mypy strict mode compliance
- **Professional OOP**: Abstract base classes, inheritance, polymorphism
- **Functional Programming**: List comprehensions, filter, map operations
- **Input Validation**: Robust error handling for all user interactions

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.14+ (3.8+ should work)
pip
```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/dnd-combat-game.git
   cd dnd-combat-game
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up OpenAI API Key (Optional - for AI narration)**
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your-api-key-here
   ```
   
   Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   
   *Note: The game works without an API key but won't have AI narration*

5. **Run the game!**
   ```bash
   python main.py
   ```

## 🎯 How to Play

1. **Create Your Character**
   - Choose your name
   - Select a race (each has unique bonuses)
   - Roll your stats (STR, DEX, CON, INT, WIS, CHA)
   - Choose 2 starting spells

2. **Main Menu Options**
   - **Fight a goblin**: Engage in turn-based combat
   - **View character**: See your stats, HP, weapons, and spells
   - **Change weapon**: Equip different weapons for varied damage
   - **Rest**: Restore HP and spell slots
   - **Quit**: Exit the game

3. **Combat**
   - Take turns attacking or casting spells
   - Manage your spell slots strategically
   - Defeat enemies to gain experience
   - Level up to increase your power!

## 🏗️ Architecture

### Project Structure
```
dnd-game/
├── dndgame/
│   ├── entity.py           # Base class for all combat entities
│   ├── character.py        # Player character with leveling
│   ├── enemy.py            # Enemy entities (Goblin, etc.)
│   ├── combat.py           # Combat system and turn management
│   ├── races.py            # Race system (Human, Elf, Dwarf, Halfling)
│   ├── weapons.py          # Weapon system with 10 weapon types
│   ├── spells.py           # Spellcasting system
│   ├── dice.py             # Dice rolling utilities
│   └── dungeon_master.py   # AI narration with OpenAI
├── tests/                  # 82 unit tests
├── main.py                 # Game entry point
└── requirements.txt        # Dependencies
```

### Design Patterns Used
- **Abstract Base Classes**: Entity as base for Character and Enemy
- **Factory Pattern**: Enemy creation (create_goblin)
- **Strategy Pattern**: Race system with interchangeable bonuses
- **Template Method**: Combat flow with customizable actions

### Key Design Decisions

#### Entity System
All combat-capable entities (Character, Enemy) inherit from an abstract `Entity` base class, ensuring consistent behavior and enabling polymorphism in the combat system.

#### Race System
Races are implemented as objects (not strings) using the Strategy pattern, making it trivial to add new races without modifying existing code.

#### Spellcasting
Spells use inheritance (DamageSpell, HealingSpell) from an abstract Spell base class, with functional programming for spell filtering.

## 🧪 Development

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=dndgame --cov-report=html

# Run specific test file
pytest tests/test_combat.py -v
```

### Type Checking
```bash
# Check all files
mypy dndgame/ --strict
mypy main.py --strict
```

### Code Formatting
```bash
# Format code
black .

# Check formatting
black . --check
```

## 📊 Technical Stats

- **Lines of Code**: 2000+ (excluding tests)
- **Test Cases**: 82
- **Code Coverage**: 77%
- **Type Safety**: 100% (mypy strict)
- **Git Commits**: 28
- **Branches Used**: 15+ feature branches
- **Python Version**: 3.14+

## 🎓 Learning Outcomes

This project demonstrates proficiency in:

### Python Programming
- ✅ Object-Oriented Programming (OOP)
- ✅ Abstract Base Classes (ABC)
- ✅ Type Hints and Static Type Checking
- ✅ Functional Programming Patterns
- ✅ Exception Handling
- ✅ File I/O and Environment Variables

### Software Engineering
- ✅ Test-Driven Development (TDD)
- ✅ Unit Testing with pytest
- ✅ Code Coverage Analysis
- ✅ Git Workflow with Feature Branches
- ✅ Clean Code Principles
- ✅ SOLID Principles
- ✅ Design Patterns

### API Integration
- ✅ OpenAI API Integration
- ✅ Asynchronous Requests
- ✅ Error Handling for External APIs
- ✅ Environment Variable Management

## 🛠️ Technologies Used

- **Python 3.14**: Core language
- **pytest**: Testing framework
- **mypy**: Static type checker
- **black**: Code formatter
- **OpenAI API**: AI-powered narration
- **python-dotenv**: Environment management

## 🤝 Contributing

This is a portfolio project, but suggestions and feedback are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🎮 Example Gameplay

```
Welcome to D&D Adventure!
🎲 AI Dungeon Master enabled! Prepare for epic narration! 🎲

Enter your character's name: Aragorn

Choose your race:
1. Human (+1 to all stats)
2. Elf (+2 DEX)
3. Dwarf (+2 CON)
4. Halfling (+2 DEX, +1 CHA)

A goblin appears!
Initiative order: ['Aragorn', 'Goblin']

--- Round 1 ---
Your turn!
1. Attack with weapon
2. Cast spell
3. Run away

📖 With a fierce battle cry, Aragorn lunges forward, his longsword 
gleaming in the dim light as he cleaves through the air, striking 
the goblin with devastating force!

💥 You hit the goblin with your Longsword for 9 damage!
🎉 VICTORY! You defeated the goblin!
✨ Gained 50 XP! (Total: 50/100)
```

## 🔮 Future Enhancements

Potential features for future development:
- [ ] More enemy types (Orcs, Dragons, etc.)
- [ ] Additional character classes (Wizard, Rogue, etc.)
- [ ] Inventory system
- [ ] Save/Load game functionality
- [ ] Multiplayer support
- [ ] Dungeon exploration
- [ ] Boss battles with unique mechanics
- [ ] Character customization (backgrounds, skills)

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- OpenAI for the GPT-4 API
- The D&D community for inspiration
- Python community for excellent tools and libraries

---

⭐ Star this repository if you found it interesting!

🎲 Happy adventuring! 🎲
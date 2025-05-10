<a name="readme-top"></a>
<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Address Parser Library</h3>

  <p align="center">
    Async Python library for street address normalization with fuzzy matching
    <br />
    <a href="#usage"><strong>Explore the docs »</strong></a>
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

A Python library for normalizing street addresses using async database operations and fuzzy string matching.

### Built With

* Python 3.11+
* aiosqlite
* SQLite

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Python 3.11+
* pip

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/005-bot/address-parser.git
   ```
2. Install the package
   ```bash
   pip install .
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

```python
import asyncio
from address_parser import AddressParser

async def main():
    async with AddressParser() as parser:
        result = await parser.normalize("пр. Ленина 25")
        if result:
            print(f"Original: {result.name}")
            print(f"Normalized: {result.normalized_name}")
            print(f"Confidence: {result.confidence:.2f}")
        else:
            print("No match found")

asyncio.run(main())
```

### Database Setup

```bash
python scripts/populate_streets.py --region "Your Region"
```

### Configuration

* Custom database path: `AddressParser(db_path="custom.db")`
* Default location: Installed as package data in `data/streets.db`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

* [ ] Improve matching algorithm accuracy
* [ ] Add support for additional address formats
* [ ] Enhance documentation with more examples

See the [open issues](https://github.com/005-bot/address-parser/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the Apache License 2.0. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Aleksandr Soloshenko - admin@005бот.рф

Project Link: [https://github.com/005-bot/address-parser](https://github.com/005-bot/address-parser)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/005-bot/address-parser.svg?style=for-the-badge
[contributors-url]: https://github.com/005-bot/address-parser/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/005-bot/address-parser.svg?style=for-the-badge
[forks-url]: https://github.com/005-bot/address-parser/network/members
[stars-shield]: https://img.shields.io/github/stars/005-bot/address-parser.svg?style=for-the-badge
[stars-url]: https://github.com/005-bot/address-parser/stargazers
[issues-shield]: https://img.shields.io/github/issues/005-bot/address-parser.svg?style=for-the-badge
[issues-url]: https://github.com/005-bot/address-parser/issues
[license-shield]: https://img.shields.io/github/license/005-bot/address-parser.svg?style=for-the-badge
[license-url]: https://github.com/005-bot/address-parser/blob/master/LICENSE

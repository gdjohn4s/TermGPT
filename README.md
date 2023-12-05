<h1 align="center">
  <br>
  <a href=""><img src="./assets/logo_new.png" alt="TermGPT" width="150" style="border-radius: 8px;"></a>
  <br>
  <br />
  TermGPT
  <br>
</h1>

<h4 align="center">A Terminal-based Client for ChatGPT! Say goodbye to the switch process between windows.</h4>

<p align="center">
  <a href="#features">Key Features</a> •
</p>

![preview](./assets/preview.gif)

![screenshot](./assets/Hero.png)

<!-- ABOUT THE PROJECT -->

## About The Project

### Overview

**TermGPT** is a streamlined, terminal-based client designed for seamless interactions with OpenAI's ChatGPT. It's born from the need to eliminate the constant window switching that developers, researchers, and enthusiasts face when jumping between their coding environment and the web-based ChatGPT interface.

### Why TermGPT?

- **Efficiency**: Stay within your terminal environment. No need to switch between windows or apps.
- **Intuitive Interface**: Designed with simplicity in mind, TermGPT ensures that the user experience is smooth, straightforward, and free of distractions.
- **Quick Access**: With TermGPT, getting a response from ChatGPT is just a command away, making it incredibly convenient for those who need instant feedback or assistance.
- **Customizable**: Being open-source, you can customize TermGPT to best fit your workflow and preferences.

### Features

- **Direct Integration**: Communicate with ChatGPT without leaving your terminal.
- **Responsive UI**: An interface that's easy to navigate and understand, ensuring a seamless chat experience.
- **Open-Source**: TermGPT is community-driven. Developers are encouraged to contribute, enhance, and tailor the project to their needs.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# TermGPT Build Instructions

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x

## Building TermGPT

Building TermGPT is straightforward. Follow these simple steps:

### Standard Build

1. Open your terminal.
2. Navigate to the root directory of the TermGPT project.
3. Run the following command:

```bash
python3 build.py
```

This will compile and create the TermGPT pip package.

### Building in a Virtual Environment

If you prefer to build within a virtual environment, follow these steps:

1. Open your terminal.
2. Navigate to the TermGPT project directory.
3. Create a virtual environment:

```
python3 -m venv myenv
```

Replace `myenv` with your preferred environment name.

4. Activate the virtual environment:

- On Windows:
  ```
  myenv\Scripts\activate
  ```
- On Unix or MacOS:
  ```
  source myenv/bin/activate
  ```

5. Once the environment is activated, run:
   python3 build.py

This builds the TermGPT package within the virtual environment.

## Running TermGPT

After successfully building the package, you can run TermGPT by simply typing the following command in your terminal:

```
termgpt -h
```

## Disclaimer

Before using the tool, it is necessary to generate an API key from OpenAI and insert it using the command:

```
termgpt setkey <YOUR_KEY>
```

The standard configuration can be found at the path: \
`/your/home/.config/termgpt/config.yaml`\
 and has the following structure:

```yaml
configuration_path: string
termGPT:
  api_key: string
  delay: float
  model: string
  role: string
  token_used: int
```

## Additional Information

- Ensure you have the necessary permissions to execute the build script.
- If you encounter any issues, please check the [Issues](https://github.com/gdjohn4s/TermGPT/issues) section or open a new issue.

---

### Built With

- [Textual](https://textual.textualize.io/)
- [Rich](https://github.com/Textualize/rich)
- [OpenAI Library](https://github.com/openai/openai-python)

## Code of Conduct

We value the participation of every member of our community and aim to create an open and welcoming environment. We are committed to fostering a positive culture, free from harassment and discrimination. Please follow our [Code of Conduct](./CODE_OF_CONDUCT.md) when interacting within this project. Adhering to these guidelines helps ensure a productive, harmonious environment for all contributors.

### License

Mit. License

<p align="right">(<a href="#readme-top">back to top</a>)</p>

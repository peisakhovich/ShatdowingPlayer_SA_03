# Sound Language Studio

[Русская версия](index.md)

## Introduction

### What is Sound Language Studio

**Sound Language Studio** is a desktop application for foreign language learning based on text and audio training.

The application combines text processing, speech synthesis, audio playback, and an interactive graphical user interface. Learning material can be automatically transformed into a sequence of actions that form a language training session.

### Project Purpose

The main purpose of Sound Language Studio is to provide a tool for independent language practice that allows users to create and perform different types of training based on learning material.

The project architecture is designed with future extensibility in mind. In particular, a training scenario is not hard-coded into the application logic. The sequence of actions is defined by the configuration in the `scenarios.json` file.

This makes it possible to modify existing scenarios and add new ones without changing the core application architecture.

### Scenario-Parameterized Finite-State Machine

The application uses a **scenario-parameterized finite-state machine** as the execution engine for language training.

A scenario defines the sequence of states and actions to be performed during a training session, while parameters determine the specific data and conditions used by those actions. As a result, the same execution mechanism can support different training scenarios.

The sequence of actions is defined in `scenarios.json`. This separates the training execution logic from the specific scenario and its content.

This approach allows a training session to be represented as a sequence of controlled states, with transitions determined by the scenario and the current parameters. In general, adding a new scenario only requires defining the corresponding sequence of actions in the configuration.

### Training Scenarios

A training scenario defines the sequence of actions performed by the application for each phrase.

The scenario configuration can use actions such as:

* `SHOW` — displays text;
* `HIDE` — hides a user interface element;
* `PLAY` — plays audio;
* `WAIT` — waits for a specified pause.

Actions can refer to different elements of the learning material and training parameters, such as `phrase_text`, `translate_text`, `pause_before_translation`, and `pause_between_sentences`.

The current `scenarios.json` configuration provides the following scenarios:

* **Shadowing**;
* **Shadowing without translation**;
* **Translation first**;
* **Reading**;
* **Dictation**.

This list is not fixed. The `scenarios.json` file provides a configuration mechanism through which the set of available scenarios can be extended and existing scenarios can be modified.

Thus, **Shadowing** is one of the application's scenarios rather than a limitation of the overall system. **Dictation** is likewise a separate scenario that uses the common application infrastructure.

**what is The Shatdowing:**  [Intro](shadowing_intro_en.md)

### Main Capabilities

At its current stage of development, Sound Language Studio provides the following capabilities:

* processing learning material;
* detecting the language of the text;
* segmenting text into phrases;
* automatically generating training plans;
* speech synthesis;
* audio caching;
* audio playback;
* executing configurable training scenarios;
* working with user learning sets;
* importing and exporting learning materials;
* managing the user session;
* user authentication;
* communication with the server-side API.

### Overall Architecture

The application consists of several major subsystems:

* **AI** — language detection, text processing, segmentation, and training plan generation;
* **Audio** — speech synthesis, audio caching, and audio playback;
* **GUI** — graphical user interface;
* **Session** — user session and learning set management;
* **API** — communication with the server-side components;
* **Core** — core application components, configuration, and system services;
* **Utils** — utility components.

The scenario mechanism plays a central role in connecting learning data with a sequence of actions defined in `scenarios.json`. This allows the same application infrastructure to support different forms of language training.

The detailed structure of individual subsystems, modules, and their APIs is documented in the **Modules** section.

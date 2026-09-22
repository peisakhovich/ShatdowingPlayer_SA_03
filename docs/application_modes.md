# Application Modes & API Configuration

Sound Language Studio can operate in different modes depending on the availability of its external services.

## Application Modes

### Local Mode

Local Mode does not require any external API services.

Available features include:

* Shadowing
* Dictation
* Text-to-Speech
* Local learning sets
* Excel import and export

This mode allows the application to be used without API keys.

### AI Mode

AI Mode is available when the OpenAI API is configured, while the Database API is unavailable or not configured.

It provides all Local Mode features plus AI-assisted learning features.

### Full Mode

Full Mode is available when both the OpenAI API and the Database API are configured and accessible.

It provides all currently implemented application features, including:

* AI-assisted learning
* Remote learning-set storage
* Database synchronization

The OpenAI API and Database API operate independently. If one service is unavailable, the other features of the application can continue to work.

## API Configuration

API configuration is performed through the `.env` file located in the application directory.

The project includes `.env_default` as a template. Create a local `.env` file based on this template and enter the required API keys.

### OpenAI API

The OpenAI API is used for AI-assisted learning features.

Users can create their own OpenAI API key and add it to the `.env` file:

```text
OPENAI_API_KEY=YourKey
```

The OpenAI API key is not provided with the application.

### Database API

The Database API provides access to the remote Sound Language Studio database.

**If you want to use the remote Database API, please contact the author of the project to obtain an API key.**

Add the received key to the `.env` file:

```text
API_KEY=YourDatabaseApiKey
```

The Database API key is not included in the public source code.

## API Keys

Both API keys are optional.

| Service      | Environment variable | Required                          |
| ------------ | -------------------- | --------------------------------- |
| OpenAI API   | `OPENAI_API_KEY`     | Only for AI features              |
| Database API | `API_KEY`            | Only for remote database features |

The application can therefore be used without either key in Local Mode.

## Security

API keys are private credentials.

* Do not commit `.env` to the Git repository.
* Do not publish API keys in screenshots or documentation.
* Keep your personal OpenAI API key private.
* Do not share a Database API key publicly.

The `.env` file is intended for local configuration and should remain outside version control.

# Google Scholar Articles Scrape to Custom UI Embed

A unified system that scrapes Google Scholar articles and provides them through a custom UI embed.

## System Architecture

The system consists of two main services:
1. **Scholar Service**: Python-based service that scrapes Google Scholar and generates BibTeX files
2. **Embed Service**: Node.js-based service that serves BibTeX files through a custom UI

## Local Development

### Prerequisites
- Docker and Docker Compose
- Node.js >= 18.0.0
- Python 3.8+
- SERPAPI Key
- Google Scholar Profile URL

### Setup

1. Clone the repository:
```bash
git clone https://github.com/jshinodea/Google-Scholar-Articles-Scrape-to-Custom-UI-Embed.git
cd Google-Scholar-Articles-Scrape-to-Custom-UI-Embed
```

2. Create a `.env` file:
```bash
# Required API keys
SERPAPI_KEY=your_serpapi_key_here
SCHOLAR_PROFILE_URL=https://scholar.google.com/citations?user=your_user_id_here&hl=en

# Optional configurations
NODE_ENV=development
FLASK_ENV=development
PORT=3000
```

3. Start the services:
```bash
docker-compose up --build
```

The services will be available at:
- Embed Service: http://localhost:3000
- Scholar Service: http://localhost:5000

## Render Deployment

1. Fork this repository

2. Create a new Blueprint Instance on Render:
   - Connect your GitHub account
   - Select the forked repository
   - Render will automatically detect the `render.yaml`

3. Configure environment variables:
   - Add your `SERPAPI_KEY` in the Render dashboard
   - Add your `SCHOLAR_PROFILE_URL` in the Render dashboard
   - Format: `https://scholar.google.com/citations?user=YOUR_USER_ID&hl=en`

4. Deploy:
   - Render will automatically build and deploy both services
   - The embed service will be accessible via a Render URL
   - The scholar service will run as a cron job at midnight

## Usage

### Embed Service
To embed the citation viewer in your website:

```html
<iframe src="https://your-render-url/embed" width="100%" height="500px"></iframe>
```

### Scholar Service
The scholar service runs automatically at midnight to update citations. You can also trigger updates manually through the API:

```bash
curl -X POST https://your-render-url/update
```

To check the current configuration:
```bash
curl https://your-render-url/config
```

## Monitoring and Logs

- Health checks are configured for both services
- Logs are available in the Render dashboard
- The embed service includes Winston logging for debugging

## Security

- CORS is properly configured for embedding
- Rate limiting is implemented on the embed service
- Environment variables are handled securely
- API keys are stored as secrets

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
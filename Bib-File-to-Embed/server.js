const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const winston = require('winston');
const path = require('path');
const fs = require('fs').promises;
const axios = require('axios');

// Configure logger
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.Console(),
        new winston.transports.File({ filename: 'error.log', level: 'error' }),
        new winston.transports.File({ filename: 'combined.log' })
    ]
});

const app = express();

// Configure rate limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100 // limit each IP to 100 requests per windowMs
});

// Middleware
app.use(cors());
app.use(express.json());
app.use(limiter);
app.use(express.static('public'));

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        service: 'embed-service'
    });
});

async function fetchFromStorage() {
    try {
        const storageKey = process.env.RENDER_STORAGE_KEY;
        if (!storageKey) {
            throw new Error('RENDER_STORAGE_KEY not set');
        }

        const response = await axios.get('https://api.render.com/v1/storage/citations.bib', {
            headers: {
                'Authorization': `Bearer ${storageKey}`
            }
        });

        return response.data;
    } catch (error) {
        logger.error('Error fetching from storage:', error);
        throw error;
    }
}

// Embed endpoint
app.get('/embed', async (req, res) => {
    try {
        const bibContent = await fetchFromStorage();
        res.render('embed', { citations: bibContent });
    } catch (error) {
        logger.error('Error serving embed:', error);
        res.status(500).json({
            status: 'error',
            message: 'Failed to load citations'
        });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    logger.error('Unhandled error:', err);
    res.status(500).json({
        status: 'error',
        message: 'Internal server error'
    });
});

// 404 handler
app.use((req, res) => {
    res.status(404).json({
        status: 'error',
        message: 'Resource not found'
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    logger.info(`Embed service listening on port ${PORT}`);
});
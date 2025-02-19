// src/setupTests.js
import '@testing-library/jest-dom';

// Optionally, silence expected console errors during tests:
jest.spyOn(console, 'error').mockImplementation(() => { });

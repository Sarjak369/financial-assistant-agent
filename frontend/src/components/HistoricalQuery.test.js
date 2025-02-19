// src/components/HistoricalQuery.test.js
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import HistoricalQuery from './HistoricalQuery';

jest.mock('axios');

describe('HistoricalQuery Component', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('fetches and displays historical data', async () => {
        const mockResponse = {
            data: {
                query: "SELECT * FROM stock_data",
                result: [
                    ["2024-02-10", "AAPL", "184.2", "185.3"],
                    ["2024-02-11", "AAPL", "185.3", "186.0"]
                ]
            }
        };
        axios.get.mockResolvedValueOnce(mockResponse);

        render(<HistoricalQuery />);

        const input = screen.getByPlaceholderText(/Enter SQL query, e.g., SELECT \* FROM stock_data/i);
        fireEvent.change(input, { target: { value: "SELECT * FROM stock_data" } });

        const button = screen.getByText(/Run Query/i);
        fireEvent.click(button);

        await waitFor(() => {
            expect(screen.getByText("SELECT * FROM stock_data")).toBeInTheDocument();
            // Check for one cell value; since "185.3" appears in two cells, getAllByText should return an array.
            const cellElements = screen.getAllByText("185.3");
            expect(cellElements.length).toBeGreaterThan(0);
        });
    });

    test('shows error if data format is invalid', async () => {
        axios.get.mockResolvedValueOnce({
            data: {
                query: "SELECT * FROM stock_data",
                result: "invalid_format"
            }
        });

        render(<HistoricalQuery />);

        const input = screen.getByPlaceholderText(/Enter SQL query, e.g., SELECT \* FROM stock_data/i);
        fireEvent.change(input, { target: { value: "SELECT * FROM stock_data" } });

        const button = screen.getByText(/Run Query/i);
        fireEvent.click(button);

        await waitFor(() => {
            expect(screen.getByText(/Invalid data format received./i)).toBeInTheDocument();
        });
    });
});

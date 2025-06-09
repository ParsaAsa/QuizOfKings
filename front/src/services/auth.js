import api from './api';

export const authService = {
    // Login user
    login: async (username, password) => {
        try {
            const response = await api.post('/api/players/login', {
                username,
                password,
            });

            const { access_token } = response.data;
            localStorage.setItem('access_token', access_token);

            return { success: true, token: access_token };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.msg || 'Login failed',
            };
        }
    },

    // Register user
    register: async (username, email, password) => {
        try {
            const response = await api.post('/api/players', {
                username,
                email,
                player_password: password,
                player_role: 'normal',
            });

            return { success: true, playerId: response.data.player_id };
        } catch (error) {
            return {
                success: false,
                error: error.response?.data?.error || 'Registration failed',
            };
        }
    },

    // Logout user
    logout: () => {
        localStorage.removeItem('access_token');
    },

    // Check if user is authenticated
    isAuthenticated: () => {
        return !!localStorage.getItem('access_token');
    },

    // Get token
    getToken: () => {
        return localStorage.getItem('access_token');
    },
};
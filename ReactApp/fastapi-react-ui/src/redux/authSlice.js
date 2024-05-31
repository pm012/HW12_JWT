import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axiosInstance from '../axiosConfig';

const initialState = {
  token: localStorage.getItem('token') || null,
  username: localStorage.getItem('username') || null,
  status: 'idle',
  error: null,
};

export const login = createAsyncThunk('auth/login', async ({ username, password }) => {
  const response = await axiosInstance.post('/api/auth/login', `username=${username}&password=${password}`, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  return response.data;
});

export const signup = createAsyncThunk('auth/signup', async (userData) => {
  const response = await axiosInstance.post('/api/auth/signup', userData);
  return response.data;
});

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: (state) => {
      state.token = null;
      state.username = null;
      localStorage.removeItem('token');
      localStorage.removeItem('username');
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.fulfilled, (state, action) => {
        state.token = action.payload.access_token;
        state.username = action.payload.username;
        localStorage.setItem('token', action.payload.access_token);
        localStorage.setItem('username', action.payload.username);
      })
      .addCase(signup.fulfilled, (state, action) => {
        state.status = 'succeeded';
      })
      .addCase(login.rejected, (state, action) => {
        state.error = action.error.message;
      })
      .addCase(signup.rejected, (state, action) => {
        state.error = action.error.message;
      });
  },
});

export const { logout } = authSlice.actions;

export default authSlice.reducer;

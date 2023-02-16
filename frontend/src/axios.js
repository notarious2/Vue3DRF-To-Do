import axios from "axios";
import { useAuthStore } from "../src/components/store/userAuth.js";

axios.defaults.baseURL = process.env.VUE_APP_BACKEND_URL;

// axios interceptor for specific URL - instance

//response interceptor
axios.interceptors.response.use(
  (res) => {
    return res;
  },
  async function (error) {
    // refresh token
    const originalRequest = error.config;
    // refresh token may have expired / no token provided
    if (
      (error.response.status === 401 &&
        error.response.data.detail === "Token is invalid or expired") ||
      error.response.data.detail ===
        "Authentication credentials were not provided."
    ) {
      const authStore = useAuthStore();
      authStore.logout();
    }
    if (
      error.response.status === 401 &&
      error.request.responseURL.includes(axios.defaults.baseURL) &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      const authStore = useAuthStore();
      // get newly assigned access token
      const newAccessToken = await authStore.refreshToken();
      // retry original request
      originalRequest.headers["Authorization"] = "Bearer " + newAccessToken;
      return axios.request(originalRequest);
    }
    return Promise.reject(error);
  }
);

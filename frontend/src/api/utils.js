import axios from 'axios';
import { HttpError } from 'react-admin';

export const apiUrl = process.env.REACT_APP_API_URL;

export const API = axios.create();

export function getCookie(name) {
  const vname = `${name}=`;
  const decodedCookie = decodeURIComponent(document.cookie);
  const ca = decodedCookie.split(';');
  for (let i = 0; i < ca.length; i += 1) {
    let c = ca[i];
    while (c.charAt(0) === ' ') c = c.substring(1, c.length);
    if (c.indexOf(vname) === 0) {
      return c.substring(vname.length, c.length);
    }
  }
  return '';
}

export function setCookie(name, value, exdays = 1) {
  const d = new Date();
  d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
  const expires = `expires=${d.toUTCString()}`;
  document.cookie = `${name}=${value};${expires};path=/`;
}

export function destroyCookie(name) {
  if (typeof window === 'undefined') { return; }
  document.cookie = `${name}=; Max-Age=-1`;
}

export function updateAccessToken() {
  return API.post(
    `${apiUrl}/users/access-tokens`,
    {},
    {
      headers: {
        Authorization: `Bearer ${getCookie('refresh_token')}`,
      },
    },
  )
    .then((resp) => setCookie('access_token', resp.data.access_token))
    .catch((error) => {
      if (error.response.status === 401) {
        return Promise.reject(new HttpError('Session expired'));
      }
      return Promise.reject(new HttpError('Неизвестная ошибка авторизации'));
    });
}

export function request(method, url, data = {}) {
  const headers = {};
  const refreshToken = getCookie('refresh_token');
  if (refreshToken) {
    headers.Authorization = `Bearer ${getCookie('access_token')}`;
  }

  return API({
    method: method.toLowerCase(),
    url: `${apiUrl}${url}`,
    params: method.toLowerCase() === 'get' ? data : {},
    data: method.toLowerCase() === 'get' ? {} : data,
    headers,
  })
    .catch((error) => {
      if (error.response && refreshToken
        && (error.response.status === 422 || error.response.status === 401)) {
        return updateAccessToken().then(() => request(method, url, data));
      }
      return Promise.reject(
        new HttpError(error.response.data.description, error.response.status, error.response.data),
      );
    });
}

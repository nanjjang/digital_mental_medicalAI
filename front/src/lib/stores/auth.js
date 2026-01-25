import { browser } from '$app/environment';
import { writable } from 'svelte/store';

const emptyState = {
  isLoggedIn: false,
  username: '',
  email: ''
};

function readFromStorage() {
  if (typeof localStorage === 'undefined') {
    return emptyState;
  }

  const token = localStorage.getItem('auth_token');
  const username = localStorage.getItem('user_username');
  const email = localStorage.getItem('user_email');

  if (!token) {
    return emptyState;
  }

  return {
    isLoggedIn: true,
    username: username || email || '',
    email: email || ''
  };
}

const auth = writable(browser ? readFromStorage() : emptyState);

function initFromStorage() {
  auth.set(readFromStorage());
}

function setAuth(user) {
  auth.set({
    isLoggedIn: true,
    username: user?.username || user?.email || '',
    email: user?.email || ''
  });
}

function clearAuth() {
  auth.set(emptyState);
}

export { auth, initFromStorage, setAuth, clearAuth };

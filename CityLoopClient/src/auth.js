export default {
    loggedIn() {
      return !!localStorage.getItem('access')
    }
  }
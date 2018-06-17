import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';

@Injectable()
export class UserService {
  isLoggedIn: boolean = false;
  redirectUrl: string = '';

  constructor(private http: HttpClient) { }

  register(email: string, password: string) {

	const httpOptions = {
	  headers: new HttpHeaders({
	    'Content-Type':  'application/json'
	  })
	};

	return this.http.post('http://127.0.0.1:8480/register', {'email': email, 'password': password});
  }

  confirm(email_hash: string, confirm_hash: string) {

	const httpOptions = {
	  headers: new HttpHeaders({
	    'Content-Type':  'application/json'
	  })
	};

	return this.http.get('http://127.0.0.1:8480/confirm/' + email_hash + '/' + confirm_hash);
  }

  sendForgot(email: string) {

	const httpOptions = {
	  headers: new HttpHeaders({
	    'Content-Type':  'application/json'
	  })
	};

	return this.http.post('http://127.0.0.1:8480/forgot', {'email': email});
  }

  checkReset(email_hash: string, reset_hash: string) {

	const httpOptions = {
	  headers: new HttpHeaders({
	    'Content-Type':  'application/json'
	  })
	};

	return this.http.get('http://127.0.0.1:8480/check_reset/' + email_hash + '/' + reset_hash);
  }

  reset(email_hash: string, reset_hash: string, password: string, repeat_password: string) {

	const httpOptions = {
	  headers: new HttpHeaders({
	    'Content-Type':  'application/json'
	  })
	};

	let post_vars = {'email_hash': email_hash, 'reset_hash': reset_hash, 'password': password, 'repeat_password': repeat_password};
	return this.http.post('http://127.0.0.1:8480/reset', post_vars);
  }

  login(email: string, password: string) {

	const httpOptions = {
	  headers: new HttpHeaders({
	    'Content-Type':  'application/json'
	  })
	};

	let post_vars = {'email': email, 'password': password};
	return this.http.post('http://127.0.0.1:8480/login', post_vars);
  }

  auth(token: string) {

	const httpOptions = {
	  headers: new HttpHeaders({
	    'Content-Type':  'application/json'
	  })
	};

	let post_vars = {'token': token};
	return this.http.post('http://127.0.0.1:8480/auth', post_vars);
  }

  checkLoggedIn() {
  	return this.isLoggedIn;
  }

}


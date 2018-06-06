import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';

@Injectable()
export class UserService {

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

}


import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';

@Injectable()
export class UserService {

  constructor(private http: HttpClient) { }

  register(login: string, password: string) {

	const httpOptions = {
	  headers: new HttpHeaders({
	    'Content-Type':  'application/json'
	  })
	};

	return this.http.post('http://127.0.0.1:8480/register', {'login': login, 'password': password});
  }

}

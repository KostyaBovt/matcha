import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';

@Injectable()
export class ApiService {

  constructor(private http: HttpClient) { }

  request(url: string, args: Object) {

	const httpOptions = {
	  headers: new HttpHeaders({
	    'Content-Type':  'application/json'
	  })
	};

	let token = localStorage.getItem('token');

	args['token'] = token;
	return this.http.post('http://127.0.0.1:8480/' + url, args);
  }

}

import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-explore',
  templateUrl: './explore.component.html',
  styleUrls: ['./explore.component.css']
})
export class ExploreComponent implements OnInit {
  test: string;

  constructor(private http: HttpClient) { }

  ngOnInit() {
  	this.test = 'hello';
  	this.http.get('http://127.0.0.1:8480').subscribe(data => {
  		console.log(data);
  	});
  }

}

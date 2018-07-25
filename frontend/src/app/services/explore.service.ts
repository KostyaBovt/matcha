import { ApiService } from './api.service'
import { Injectable } from '@angular/core';

@Injectable()
export class ExploreService {

  constructor(private apiService: ApiService) { }

  searchMates(args) {
  	return this.apiService.request('explore/search_mates', args);
  }

  like(mate_id) {
  	let args = {'mate_id': mate_id}
  	return this.apiService.request('explore/like', args);
  }
}

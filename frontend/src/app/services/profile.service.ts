import { ApiService } from './api.service'
import { Injectable } from '@angular/core';

@Injectable()
export class ProfileService {

  constructor(private apiService: ApiService) { }

  get() {

	return this.apiService.request('profile/get', {});
  }

}


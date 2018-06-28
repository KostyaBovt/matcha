import { ApiService } from './api.service'
import { Injectable } from '@angular/core';

@Injectable()
export class ProfileService {

  constructor(private apiService: ApiService) { }

  get() {
	return this.apiService.request('profile/get', {});
  }

  update(
  	username: string,
	fname: string,
	sname: string,
	gender: number,
	sex_preference: number,
	birth: string,
	phone: string,
	bio: string,
	interests: string
  ) {
  	let args = {
  		'username': username,
		'fname': fname,
		'sname': sname,
		'gender': gender,
		'sex_preference': sex_preference
		'birth': birth,
		'phone': phone,
		'bio': bio,
		'interests': interests
  	}
  	return this.apiService.request('profile/update', args)
  }

}


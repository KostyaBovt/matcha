import { ApiService } from './api.service'
import { Injectable } from '@angular/core';

@Injectable()
export class ExploreService {

  constructor(private apiService: ApiService) { }

  searchMates(args) {
    return this.apiService.request('explore/search_mates', args);
  }

  searchConnections(args) {
    return this.apiService.request('explore/search_connections', args);
  }

  getMate(mate_id, to_log) {
    let args = {
      'mate_id': mate_id,
      'to_log': to_log
    }
    return this.apiService.request('explore/get_mate', args);
  }

  like(mate_id) {
    let args = {'mate_id': mate_id}
    return this.apiService.request('explore/like', args);
  }

  unlike(mate_id) {
    let args = {'mate_id': mate_id}
    return this.apiService.request('explore/unlike', args);
  }

  dislike(mate_id) {
    let args = {'mate_id': mate_id}
    return this.apiService.request('explore/dislike', args);
  }

  undislike(mate_id) {
    let args = {'mate_id': mate_id}
    return this.apiService.request('explore/undislike', args);
  }

  report(mate_id) {
    let args = {'mate_id': mate_id}
    return this.apiService.request('explore/report', args);
  }

}

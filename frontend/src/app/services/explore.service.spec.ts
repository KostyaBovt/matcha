import { TestBed, inject } from '@angular/core/testing';

import { ExploreService } from './explore.service';

describe('ExploreService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ExploreService]
    });
  });

  it('should be created', inject([ExploreService], (service: ExploreService) => {
    expect(service).toBeTruthy();
  }));
});

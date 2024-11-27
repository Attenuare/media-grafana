import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class MoviesService {
  baseUrl: string;

  constructor(private http: HttpClient) {
    this.baseUrl = 'http://localhost:5000'; 
  }


  getMovies(): Observable<any> {
    return this.http.get(`${this.baseUrl}/get-movies`);
  }
  
}

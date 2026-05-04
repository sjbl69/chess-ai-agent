import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AiService {

  constructor(private http: HttpClient) {}

  getMoves(fen: string): Observable<any> {
    return this.http.get(
      `http://127.0.0.1:8000/api/v1/moves?fen=${encodeURIComponent(fen)}`
    );
  }
}
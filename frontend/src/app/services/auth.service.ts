import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { switchMap, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private TOKEN_KEY = 'access_token';

  constructor(private http: HttpClient) {}

  login(username: string, password: string) {
    return this.http.post<any>('http://localhost:8000/api/token/', {
      username,
      password
    }).pipe(
      switchMap(tokenResponse => {
        localStorage.setItem('access_token', tokenResponse.access);
        localStorage.setItem('refresh_token', tokenResponse.refresh);

        return this.http.get<any>('http://localhost:8000/api/accounts/current_user');
      }),
      tap(userResponse => {
        localStorage.setItem('role', userResponse.role);
      })
    );
  }

  logout() {
    localStorage.removeItem(this.TOKEN_KEY);
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  getRole(): string | null {
    return localStorage.getItem('role');
  }
}

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GisService {

  constructor(private http: HttpClient) {}

  getFloodZones(): Observable<any> {
    return this.http.get(`${environment.apiUrl}/gis/flood-zones/`);
  }

  getIncidents(): Observable<any> {
    return this.http.get(`${environment.apiUrl}/incidents/flood_incidents/`);
  }

  createIncidents(payload: any): Observable<any> {
    return this.http.post(`${environment.apiUrl}/incidents/flood_incidents/`, payload)
  }

  updateIncidentStatus(id: number, status: string) {
    return this.http.patch(
      `${environment.apiUrl}/incidents/flood_incidents/${id}/status/`,
      { status: status }
    );
  }

  getIncidentsByRiskZone(riskLevel: string) {
    return this.http.get(
      `${environment.apiUrl}/incidents/filter_by_risk_zone/?risk_level=${riskLevel}`
    );
  }


}

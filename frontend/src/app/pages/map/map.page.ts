import { Component, AfterViewInit } from '@angular/core';
import * as L from 'leaflet';
import { GisService } from '../../services/gis.service';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

delete (L.Icon.Default.prototype as any)._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'assets/images/marker-icon-2x.png',
  iconUrl: 'assets/images/marker-icon.png',
  shadowUrl: 'assets/images/marker-shadow.png'
});

@Component({
  selector: 'app-map',
  templateUrl: './map.page.html',
  styleUrls: ['./map.page.scss']
})
export class MapPage implements AfterViewInit {

  private map!: L.Map;
  private incidentLayer!: L.GeoJSON;

  selectedLat!: number;
  selectedLng!: number;
  showForm = false;

  severity = 1;
  description = '';

  canCreateIncident = false;
  canUpdateStatus = false;

  selectedRiskLevel: string = '';


  constructor(private gisService: GisService, private authService: AuthService, private router: Router) {}

  ngAfterViewInit() {
    this.initMap();
    this.loadFloodZones();
    this.loadIncidents();

    const role = this.authService.getRole();

    this.canCreateIncident = role === 'FIELD_RESPONDER' || role === 'NGO';
    this.canUpdateStatus = role === 'COMMAND_CENTER';

    if (this.canCreateIncident) {
      this.map.on('click', (e: any) => {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;

        this.openIncidentForm(lat, lng);
      });
    }

    (window as any).updateStatus = (id: number) => {
      const select = document.getElementById(`status-${id}`) as HTMLSelectElement;
      const status = select.value;
      this.updateIncidentStatus(id, status);
    };
  }

  openIncidentForm(lat: number, lng: number) {
    this.selectedLat = lat;
    this.selectedLng = lng;
    this.showForm = true;
  }

  private initMap() {
    this.map = L.map('map').setView([13.0827, 80.2707], 10); // Example: Chennai

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(this.map);
  }

  filterByRiskZone() {
    if (!this.selectedRiskLevel) {
      this.loadIncidents(); // fallback to all incidents
      return;
    }

    this.gisService.getIncidentsByRiskZone(this.selectedRiskLevel)
      .subscribe({
        next: (geojson: any) => {
          this.clearIncidentLayer();
          this.renderIncidents(geojson);
        },
        error: err => {
          alert('Error fetching filtered incidents');
        }
      });
  }


  private loadFloodZones() {
    this.gisService.getFloodZones().subscribe({
      next: (geojson: any) => {
        L.geoJSON(geojson, {
          style: (feature: any) => ({
            color: this.getRiskColor(feature.properties.risk_level),
            weight: 2,
            fillOpacity: 0.5
          }),
          onEachFeature: (feature, layer) => {
            layer.bindPopup(`
              <b>${feature.properties.name}</b><br/>
              Risk Level: ${feature.properties.risk_level}
            `);
            layer.on('click', (e: any) => {
              if (this.canCreateIncident) {
                const lat = e.latlng.lat;
                const lng = e.latlng.lng;
                this.openIncidentForm(lat, lng);
              }

            });
          }
        }).addTo(this.map);
      }
    });
  }


  private loadIncidents() {
    this.gisService.getIncidents().subscribe({
      next: (geojson: any) => {
        this.clearIncidentLayer();
        this.renderIncidents(geojson);
      }
    });
  }

  private renderIncidents(geojson: any) {
    this.incidentLayer = L.geoJSON(geojson, {

      pointToLayer: (feature, latlng) =>
        L.circleMarker(latlng, {
          radius: 8,
          fillColor: this.getIncidentColor(feature.properties.status),
          color: '#000',
          weight: 1,
          fillOpacity: 0.9
        }),

      onEachFeature: (feature, layer) => {

        let popupContent = `
          <b>Incident</b><br/>
          ${feature.properties.description}<br/>
          Status: ${feature.properties.status}<br/>
        `;

        if (this.canUpdateStatus) {
          popupContent += `
            <select id="status-${feature.id}">
              <option value="VERIFIED">Verified</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="RESOLVED">Resolved</option>
              <option value="REJECTED">Rejected</option>
            </select>
            <button onclick="window.updateStatus(${feature.id})">
              Update
            </button>
          `;
        }

        layer.bindPopup(popupContent);
      }

    }).addTo(this.map);
  }

  private clearIncidentLayer() {
    if (this.incidentLayer) {
      this.map.removeLayer(this.incidentLayer);
    }
  }



  private getIncidentColor(status: string): string {
    switch (status) {
      case 'REPORTED': return 'gray';
      case 'VERIFIED': return 'blue';
      case 'IN_PROGRESS': return 'orange';
      case 'RESOLVED': return 'green';
      case 'REJECTED': return 'red';
      default: return 'black';
    }
  }

  submitIncident() {
    const payload = {
      location: {
        type: 'Point',
        coordinates: [this.selectedLng, this.selectedLat]  // IMPORTANT: lon, lat
      },
      severity: this.severity,
      description: this.description
    };

    this.gisService.createIncidents(payload).subscribe({
        next: () => {
          this.showForm = false;
          this.loadIncidents(); // reload markers
        },
        error: err => {
          alert('Error creating incident');
        }
      });
  }

  updateIncidentStatus(id: number, status: string) {
    this.gisService.updateIncidentStatus(id, status).subscribe({
      next: () => {
        alert('Status Updated');
        this.loadIncidents();
      },
      error: () => {
        alert('Error updating status');
      }
    });
  }




  private getRiskColor(level: string): string {
    switch (level) {
      case 'HIGH': return 'red';
      case 'MEDIUM': return 'orange';
      case 'LOW': return 'yellow';
      default: return 'blue';
    }
  }

  logout() {
    this.authService.logout();
  }
}

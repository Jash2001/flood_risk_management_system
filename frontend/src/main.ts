import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app/app.module';

import './app/services/leaflet-icon-fix';

platformBrowserDynamic().bootstrapModule(AppModule)
  .catch(err => console.log(err));

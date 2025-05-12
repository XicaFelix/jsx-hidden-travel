import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

const customIcon = new L.Icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});

const DisplayMap = ({ userLocation, suggestion }) => {
  const center = userLocation
    ? [userLocation.latitude, userLocation.longitude]
    : [37.7749, -122.4194]; // fallback to San Francisco

  const positions = suggestion?.places?.map(place => [place.lat, place.lng]);

  return (
    <MapContainer center={center} zoom={12} scrollWheelZoom={true} style={{ height: '400px', width: '100%' }}>
      <TileLayer
        url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
        attribution='&copy; OpenStreetMap contributors'
      />

      {userLocation && (
        <Marker position={center} icon={customIcon}>
          <Popup>You are here</Popup>
        </Marker>
      )}

      {suggestion?.places?.map((place, index) => (
        <Marker key={index} position={[place.lat, place.lng]} icon={customIcon}>
          <Popup>
            <strong>{place.name}</strong><br />
            {place.description}
          </Popup>
        </Marker>
      ))}

      {userLocation && positions?.length > 0 && (
        <Polyline positions={[center, ...positions]} color="blue" />
      )}
    </MapContainer>
  );
};

export default DisplayMap;

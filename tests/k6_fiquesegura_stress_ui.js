// Conteúdo do arquivo
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  // Cenário de carga -> ramp-up, sustain, ramp-down.
  // Ajuste os valores conforme sua infra de staging.
  stages: [
    { duration: '1m', target: 100 },   // aquecer: 10 VUs
    // { duration: '5m', target: 2000 },   // carga principal: 2000 VUs
    { duration: '5m', target: 5000 },   // carga principal: 3000 VUs
    // { duration: '5m', target: 10000 },   // carga principal: 3000 VUs
  ],

  // Limites (thresholds) para falha do teste
  thresholds: {
    // 95% das requisições deve estar abaixo de 500ms
    http_req_duration: ['p(95)<1500', 'p(99)<2000'],
    // taxa de requisições com falha (status >= 400) abaixo de 1%
    'http_req_failed': ['rate<0.1'],
  },

};

const BASE = __ENV.BASE_URL || 'http://localhost:8501';

export default function () {
  // 1) Acessa a página inicial
  let res = http.get(`${BASE}/`);
  check(res, {
    'home status 200': (r) => r.status === 200,
    'home contém <title>Streamlit</title>': (r) => r.body && r.body.includes('<title>Streamlit</title>'),
  });

  // 2) Simula navegação por query param
  res = http.get(`${BASE}/?page=dados`);
  check(res, {
    'dados page status 200': (r) => r.status === 200,
  });

  // 3) Puxa algum recurso estático (favicon)
  http.get(`${BASE}/favicon.ico`);

}


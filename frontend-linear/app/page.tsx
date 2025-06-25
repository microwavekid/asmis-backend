// PATTERN_REF: FRONTEND_ROUTING_PATTERN
// DECISION_REF: DEC_2025-06-24_002: Redirect to new v0 intelligence UI

import { redirect } from 'next/navigation'

export default function RootPage() {
  // Redirect to the new intelligence deals page
  redirect('/deals')
}
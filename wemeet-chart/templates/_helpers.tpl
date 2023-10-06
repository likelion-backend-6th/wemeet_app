{{/*
Expand the name of the chart.
*/}}
{{- define "wemeet.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "wemeet.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{- define "wemeet.db.fullname" -}}
{{- $name := .Chart.Name }}
{{- if contains $name .Release.Name }}
{{- printf "%s-%s" "db" .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s-%s" "db" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "wemeet.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "wemeet.labels" -}}
helm.sh/chart: {{ include "wemeet.chart" . }}
{{ include "wemeet.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "wemeet.selectorLabels" -}}
app.kubernetes.io/name: {{ include "wemeet.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}


{{- define "wemeet.db.labels" -}}
helm.sh/chart: {{ include "wemeet.chart" . }}
{{ include "wemeet.db.selectorLabels" . }}
release: {{ .Release.Name }}
app.kubernetes.io/managed-by: helm
{{- end }}

{{- define "wemeet.db.selectorLabels" -}}
app: db-{{ .Release.Name }}
{{- end }}

{{- define "flask-app.name" -}}{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}{{- end }}
{{- define "flask-app.fullname" -}}{{- if .Values.fullnameOverride }}{{ .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}{{- else }}{{ printf "%s-%s" .Release.Name (include "flask-app.name" .) | trunc 63 | trimSuffix "-" }}{{- end }}{{- end }}

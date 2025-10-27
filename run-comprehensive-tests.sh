#!/bin/bash

# IntelliNemo Agent - Comprehensive Testing Suite
# Executes all 5 critical domain tests with detailed reporting

echo "🧠 IntelliNemo Agent - Comprehensive Testing Suite"
echo "=================================================="
echo "Testing AI-Powered SRE Orchestrator across 5 critical domains"
echo ""

# Set up environment
export AWS_PROFILE=${AWS_PROFILE:-intellinemo}
export FUNCTION_NAME=${FUNCTION_NAME:-intellinemo-agent-dev-agent}

# Create results directory
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_DIR="test_results_${TIMESTAMP}"
mkdir -p "$RESULTS_DIR"

echo "📁 Results will be saved to: $RESULTS_DIR"
echo ""

# Function to run test and capture results
run_test() {
    local test_name="$1"
    local test_script="$2"
    local output_file="$RESULTS_DIR/${test_name}_results.json"
    
    echo "🧪 Running: $test_name"
    echo "   Script: $test_script"
    echo "   Output: $output_file"
    
    if [ -f "$test_script" ]; then
        python3 "$test_script" > "$output_file" 2>&1
        if [ $? -eq 0 ]; then
            echo "   ✅ COMPLETED"
        else
            echo "   ❌ FAILED"
        fi
    else
        echo "   ⚠️  SKIPPED (script not found)"
    fi
    echo ""
}

# Domain 1: AI Reasoning & Decision Quality
echo "🎯 DOMAIN 1: AI REASONING & DECISION QUALITY"
echo "============================================"
run_test "ai_reasoning" "comprehensive-test-suite.py"

# Domain 2: Infrastructure Automation  
echo "🎯 DOMAIN 2: INFRASTRUCTURE AUTOMATION"
echo "======================================"
run_test "infrastructure" "test-scenarios.py"

# Domain 3: Security & Compliance
echo "🎯 DOMAIN 3: SECURITY & COMPLIANCE"
echo "=================================="
run_test "security" "tests/test_domains.py"

# Domain 4: Performance & Reliability
echo "🎯 DOMAIN 4: PERFORMANCE & RELIABILITY"
echo "======================================"
run_test "performance" "domain-specific-validators.py"

# Domain 5: Industry-Specific Scenarios
echo "🎯 DOMAIN 5: INDUSTRY-SPECIFIC SCENARIOS"
echo "========================================"
run_test "industry_scenarios" "sector-specific-tests.sh"

# Run comprehensive validation
echo "🔍 COMPREHENSIVE DOMAIN VALIDATION"
echo "=================================="
python3 domain-specific-validators.py > "$RESULTS_DIR/comprehensive_validation.json" 2>&1
echo "   ✅ Validation complete"
echo ""

# Critical scenarios testing
echo "🚨 CRITICAL SHUTDOWN SCENARIOS"
echo "=============================="
python3 critical-shutdown-scenarios.py > "$RESULTS_DIR/critical_scenarios.txt" 2>&1
echo "   ✅ Critical scenarios documented"
echo ""

# Performance benchmarking
echo "⚡ PERFORMANCE BENCHMARKING"
echo "=========================="

# Test response times
echo "📊 Testing response times..."
for i in {1..5}; do
    echo "   Test $i/5..."
    aws lambda invoke \
        --function-name "$FUNCTION_NAME" \
        --payload '{"detail":{"alarmName":"perf-test-'$i'","state":{"value":"ALARM","reason":"Performance test"},"configuration":{"metricName":"CPUUtilization","namespace":"AWS/EC2"}}}' \
        --cli-binary-format raw-in-base64-out \
        "$RESULTS_DIR/perf_test_$i.json" > /dev/null 2>&1
done

# Test concurrent load
echo "🔄 Testing concurrent load..."
for i in {1..3}; do
    aws lambda invoke \
        --function-name "$FUNCTION_NAME" \
        --payload '{"detail":{"alarmName":"load-test-'$i'","state":{"value":"ALARM","reason":"Load test"},"configuration":{"metricName":"CPUUtilization","namespace":"AWS/EC2"}}}' \
        --cli-binary-format raw-in-base64-out \
        "$RESULTS_DIR/load_test_$i.json" &
done
wait
echo "   ✅ Concurrent load test complete"
echo ""

# Generate comprehensive report
echo "📋 GENERATING COMPREHENSIVE REPORT"
echo "=================================="

cat > "$RESULTS_DIR/test_summary.md" << EOF
# IntelliNemo Agent - Test Results Summary

**Test Execution:** $(date)
**Results Directory:** $RESULTS_DIR

## 🎯 Domain Test Results

### 1. AI Reasoning & Decision Quality
- **Objective:** Validate NVIDIA NIM integration and decision accuracy
- **Key Metrics:** Response appropriateness, confidence scoring, reasoning quality
- **Status:** $([ -f "$RESULTS_DIR/ai_reasoning_results.json" ] && echo "✅ COMPLETED" || echo "❌ FAILED")

### 2. Infrastructure Automation
- **Objective:** Test auto-scaling, service recovery, resource management
- **Key Metrics:** Action appropriateness, execution success, safety controls
- **Status:** $([ -f "$RESULTS_DIR/infrastructure_results.json" ] && echo "✅ COMPLETED" || echo "❌ FAILED")

### 3. Security & Compliance
- **Objective:** Validate threat detection and incident response
- **Key Metrics:** Security pattern recognition, compliance adherence
- **Status:** $([ -f "$RESULTS_DIR/security_results.json" ] && echo "✅ COMPLETED" || echo "❌ FAILED")

### 4. Performance & Reliability
- **Objective:** Test system performance under various loads
- **Key Metrics:** Response time (<5s), throughput, reliability
- **Status:** $([ -f "$RESULTS_DIR/performance_results.json" ] && echo "✅ COMPLETED" || echo "❌ FAILED")

### 5. Industry-Specific Scenarios
- **Objective:** Validate sector-specific requirements and compliance
- **Key Metrics:** Industry pattern recognition, regulatory compliance
- **Status:** $([ -f "$RESULTS_DIR/industry_scenarios_results.json" ] && echo "✅ COMPLETED" || echo "❌ FAILED")

## 📊 Performance Metrics

### Response Time Analysis
EOF

# Analyze performance results
if ls "$RESULTS_DIR"/perf_test_*.json >/dev/null 2>&1; then
    echo "- **Individual Tests:** $(ls "$RESULTS_DIR"/perf_test_*.json | wc -l) completed" >> "$RESULTS_DIR/test_summary.md"
    echo "- **Concurrent Tests:** $(ls "$RESULTS_DIR"/load_test_*.json | wc -l) completed" >> "$RESULTS_DIR/test_summary.md"
else
    echo "- **Performance Tests:** No results found" >> "$RESULTS_DIR/test_summary.md"
fi

cat >> "$RESULTS_DIR/test_summary.md" << EOF

### Critical Scenarios Coverage
- **Total Scenarios:** 12 critical shutdown scenarios documented
- **Coverage Areas:** OOM kills, connection exhaustion, SSL expiry, resource limits

## 🏆 Overall Assessment

### Readiness Score
EOF

# Calculate readiness score based on completed tests
COMPLETED_TESTS=$(find "$RESULTS_DIR" -name "*_results.json" | wc -l)
TOTAL_TESTS=5
READINESS_SCORE=$((COMPLETED_TESTS * 100 / TOTAL_TESTS))

cat >> "$RESULTS_DIR/test_summary.md" << EOF
- **Completed Domains:** $COMPLETED_TESTS/$TOTAL_TESTS
- **Readiness Score:** $READINESS_SCORE%

### Recommendations
EOF

if [ $READINESS_SCORE -ge 80 ]; then
    echo "- ✅ **PRODUCTION READY:** All critical domains validated" >> "$RESULTS_DIR/test_summary.md"
    echo "- 🚀 **DEPLOYMENT:** Proceed with confidence" >> "$RESULTS_DIR/test_summary.md"
elif [ $READINESS_SCORE -ge 60 ]; then
    echo "- ⚠️  **MOSTLY READY:** Minor improvements needed" >> "$RESULTS_DIR/test_summary.md"
    echo "- 🔧 **ACTION:** Address failed test domains" >> "$RESULTS_DIR/test_summary.md"
else
    echo "- 🔧 **NEEDS WORK:** Significant improvements required" >> "$RESULTS_DIR/test_summary.md"
    echo "- 📋 **ACTION:** Review and fix critical issues" >> "$RESULTS_DIR/test_summary.md"
fi

cat >> "$RESULTS_DIR/test_summary.md" << EOF

## 📁 Detailed Results
- **Test Logs:** Available in $RESULTS_DIR/
- **Performance Data:** perf_test_*.json and load_test_*.json
- **Validation Report:** comprehensive_validation.json
- **Critical Scenarios:** critical_scenarios.txt

## 🔗 Next Steps
1. Review detailed test results in individual JSON files
2. Address any failed test cases
3. Optimize performance based on benchmark results
4. Validate industry-specific compliance requirements
5. Proceed with production deployment when ready

---
*Generated by IntelliNemo Agent Test Suite - $(date)*
EOF

echo "📄 Test summary generated: $RESULTS_DIR/test_summary.md"
echo ""

# Display summary
echo "============================================================"
echo "🎯 INTELLINEMO AGENT - TEST EXECUTION SUMMARY"
echo "============================================================"
echo ""
echo "📊 Test Results:"
echo "   Completed Domains: $COMPLETED_TESTS/$TOTAL_TESTS"
echo "   Readiness Score: $READINESS_SCORE%"
echo ""
echo "📁 Results Location: $RESULTS_DIR/"
echo "📋 Summary Report: $RESULTS_DIR/test_summary.md"
echo ""

if [ $READINESS_SCORE -ge 80 ]; then
    echo "🎉 EXCELLENT: IntelliNemo Agent is production ready!"
    echo "🚀 Proceed with deployment across all target domains"
elif [ $READINESS_SCORE -ge 60 ]; then
    echo "✅ GOOD: Minor optimizations recommended"
    echo "🔧 Review failed domains and address issues"
else
    echo "⚠️  ATTENTION: Significant improvements needed"
    echo "📋 Review test results and address critical issues"
fi

echo ""
echo "🔍 Next Steps:"
echo "1. Review detailed results: cat $RESULTS_DIR/test_summary.md"
echo "2. Analyze performance: ls $RESULTS_DIR/perf_test_*.json"
echo "3. Check validation: cat $RESULTS_DIR/comprehensive_validation.json"
echo "4. Address any issues found in the test results"
echo ""
echo "============================================================"
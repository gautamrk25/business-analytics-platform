export function ChecklistPanel() {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold">MLOps Best Practices</h2>
        <span className="bg-blue-100 text-blue-800 text-sm font-medium px-3 py-1 rounded">
          0 Selected
        </span>
      </div>
      
      <div className="space-y-4">
        <div className="border rounded p-4 hover:bg-gray-50 cursor-pointer">
          <h3 className="font-medium">Configure compute resources</h3>
          <p className="text-sm text-gray-600 mt-1">
            Set up and configure necessary compute resources for ML workloads
          </p>
        </div>
        
        <div className="border rounded p-4 hover:bg-gray-50 cursor-pointer">
          <h3 className="font-medium">Setup monitoring</h3>
          <p className="text-sm text-gray-600 mt-1">
            Implement monitoring and alerting for ML systems
          </p>
        </div>
      </div>
    </div>
  )
} 